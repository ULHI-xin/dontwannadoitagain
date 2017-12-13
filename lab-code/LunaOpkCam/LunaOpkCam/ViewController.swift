//
//  ViewController.swift
//  LunaOpkCam
//
//  Created by 欣 赵 on 21/11/2017.
//  Copyright © 2017 ZX. All rights reserved.
//
import AVFoundation
import UIKit

let C_STD_VARIANCE: CGFloat = 0.4
let C_DIFF: CGFloat = 10
let SMOOTH_SIZE: Int = 5
let CONF_LEVEL: CGFloat = 0.6
let C_WIDTH_MIN: Int = 8
let C_WIDTH_MAX: Int = 18
let C_STD: CGFloat = 6

struct m_RGBColor // My own data-type to hold the picture information
{
    var Alpha: UInt8 = 255
    var Red:   UInt8 = 0
    var Green: UInt8 = 0
    var Blue:  UInt8 = 0
}

class LnMath {
    static func mean(a: [CGFloat]) -> CGFloat {
        return a.reduce(0, +) / CGFloat(a.count)
    }
    static func rangedMean(a: [CGFloat], start: Int, end: Int) -> CGFloat {
        return a[start..<end].reduce(0, +) / CGFloat(end - start)
    }

    /* std = sqrt(mean(abs(x - x.mean())**2)) */
    static func std(a: [CGFloat]) -> CGFloat {
        let mean = self.mean(a: a)
        let result = sqrt(self.mean(a: a.map { (_a) -> CGFloat in pow(_a - mean, 2) }))
        return result
    }
    static func stdX(a: [CGFloat], w: Int, h: Int) -> [CGFloat] {
        var result = [CGFloat](repeating: 0, count:w)
        for x in 0 ..< w {
            var col = [CGFloat](repeating: 0, count:h)
            for y in 0 ..< h {
                col[y] = a[w * y + x]
            }
            result[x] = std(a: col)
        }
        return result
    }
    static func median(a: [CGFloat]) -> CGFloat {
        if a.count % 2 == 1 {
            return a.sorted()[a.count / 2]
        } else {
            let s = a.sorted()
            return (s[a.count / 2 - 1] + s[a.count / 2]) / 2
        }
    }
    static func medianX(a: [CGFloat], w: Int, h: Int) -> [CGFloat] {
        var result = [CGFloat](repeating: 0, count:w)
        for x in 0 ..< w {
            var col = [CGFloat](repeating: 0, count:h)
            for y in 0 ..< h {
                col[y] = a[w * y + x]
            }
            result[x] = median(a: col)
        }
        return result
    }
    static func centerWindowRollingMean(a: [CGFloat], w: Int) -> [CGFloat] {
        let lExt = w / 2, rExt = w % 2 == 1 ? w / 2 : w / 2 - 1
        return a.enumerated().map({ (idx, v) -> CGFloat in
            if idx - lExt < 0 || idx + rExt >= a.count {
                return CGFloat.nan
            } else {
                return a[idx - lExt ... idx + rExt].reduce(0, +) / CGFloat(w)
            }
        })
    }
}

class LineDetector {
    static func findPosRegion(s: [CGFloat], minW: Int, maxW: Int,
            confLv: CGFloat = CONF_LEVEL, smooth: Int = SMOOTH_SIZE) -> [[String: CGFloat]] {
        let smoothed = LnMath.centerWindowRollingMean(a: s, w: smooth)
        var regions: [[String: CGFloat]] = []
        var start = -1, end = -1
        for i in 0 ..< smoothed.count {
            if smoothed[i] <= 0.000001 && start >= 0 {
                end = i
                let w = end - start
                let area = LnMath.rangedMean(a: smoothed, start: start, end: end)
                if minW < w && w < maxW && area > confLv {
                    regions.append(["start": CGFloat(start), "end": CGFloat(end), "width": CGFloat(w), "val": area])
                }
                start = -1
                end = -1
            } else if smoothed[i] > 0 && start < 0 {
                start = i
            }
        }
        if start >= 0 {
            end = smoothed.count
            let w = end - start
            let area = LnMath.rangedMean(a: smoothed, start: start, end: end)
            if minW < w && w < maxW && area > confLv {
                regions.append(["start": CGFloat(start), "end": CGFloat(end), "width": CGFloat(w), "val": area])
            }
        }
        return regions
    }

    static func cLineLeftRight(pixels: [UInt8], w: Int) -> [String: Any] {
        let h = pixels.count / w
//        let yStart = h * 3 / 8, yEnd = h * 5 / 8
        let yStart = h * 5 / 12, yEnd = h * 7 / 12
        let croppedPixels = pixels[yStart * w ..< yEnd * w].map { (p) -> CGFloat in CGFloat(p) }

        let scnb = Scanable(pixels: croppedPixels, w: w)
        if scnb.stdVar > C_STD_VARIANCE {
            return ["rc": 1, "start": 0, "end": 0]
        }
        let isLine = scnb.diff.map { (d) -> CGFloat in d < -C_DIFF ? 1 : 0 }
        let lines = self.findPosRegion(s: isLine, minW: C_WIDTH_MIN, maxW: C_WIDTH_MAX)

        var result : [[String: CGFloat]] = []
        for l in lines {
            if CGFloat(w) * 0.5 <= l["start"]! && CGFloat(w) * 0.8 >= l["start"]! &&
                    scnb.rangedStdMean(start: Int(l["start"]!), end: Int(l["end"]!)) < C_STD {
                if result.count == 0 {
                    result.append(l)
                } else {
                    return ["rc": 2, "start": 0, "end": 0,
                            "isLine": isLine, "lines": lines,
                            "std": scnb.std]
                }
            }
        }
        if result.count == 0 {
            return ["rc": 3, "start": 0, "end": 0,
                    "isLine": isLine, "lines": lines,
                    "std": scnb.std]
        }
        return ["rc": 0, "start": Int(result[0]["start"]!), "end": Int(result[0]["end"]!),
                "isLine": isLine, "lines": lines,
                "std": scnb.std]
    }
}

struct Scanable {
    let pixels: [CGFloat]
    let w: Int
    let h: Int
    let stdMean: CGFloat
    let diff: [CGFloat]
    let std: [CGFloat]
    let stdVar: CGFloat

    init(pixels: [CGFloat], w: Int) {
        self.pixels = pixels
        self.w = w
        self.h = pixels.count / w
        let _stdMean = LnMath.median(a: LnMath.stdX(a: pixels, w: w, h: h))
        stdMean = _stdMean
        let _medianX = LnMath.medianX(a: pixels, w: w, h: h)
        let _globalMedian = LnMath.median(a: pixels)
        diff = _medianX.map({ mx in
            (mx - _globalMedian) / _stdMean
        })
        std = LnMath.stdX(a: pixels, w: w, h: h).map({ sx in
            sx / _stdMean
        })
        stdVar = LnMath.mean(a: LnMath.stdX(a: pixels, w: w, h: h)) / LnMath.std(a: pixels)
    }

    func rangedStdMean(start: Int, end: Int) -> CGFloat {
        return LnMath.rangedMean(a: self.std, start: start, end: end)
    }
}

class ViewController: UIViewController {
    var captureSession: AVCaptureSession?
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    var intervalCtrl = 0
    @IBOutlet weak var previewView: UIView!
    @IBOutlet weak var searchArea: UIImageView!
    @IBOutlet weak var recognizedImage2: UIImageView!
    @IBOutlet weak var recognizedImage: UIImageView!
    @IBOutlet weak var opkFrameView: UIView!
    @IBOutlet weak var resultC: UIView!
    @IBOutlet weak var cLineOverlay: UIView!
    @IBOutlet weak var plotView: UIView!
    override func viewDidLoad() {
        super.viewDidLoad()

        print(LnMath.std(a: [1, 7,245,244,62,123]))

        let s: [CGFloat] = [242,
 183,
 57,
 69,
 16,
 240,
 134,
 2,
 130,
 97,
 231,
 181,
 48,
 243,
 23,
 147,
 192,
 93,
 32,
 142,
 96,
 64,
 66,
 1,
 163,
 202,
 211,
 6,
 4,
 118,
 164,
 42,
 37,
 92,
 34,
 77,
 219,
 159,
 209,
 153]
        print("stdX")
        print(LnMath.stdX(a: s, w: 10, h: 4))
        print("median of stdX")
        print(LnMath.median(a: LnMath.stdX(a: s, w: 10, h: 4)))
        print("medianX")
        print(LnMath.medianX(a: s, w: 10, h: 4))
        print("LnMath.centerWindowRollingMean(a: s, w: 3)")
        print(LnMath.centerWindowRollingMean(a: s, w: 3))

        let scnb = Scanable(pixels: s, w: 10)
        print("scnb.stdMean")
        print(scnb.stdMean)
        print("scnb.diff")
        print(scnb.diff)
        print("scnb.std")
        print(scnb.std)
        print("scnb.stdVar")
        print(scnb.stdVar)
        print("scnb.rangedStdMean(35, 79)")
        print(scnb.rangedStdMean(start: 5, end: 9))

        opkFrameView.layer.borderColor = UIColor.cyan.cgColor
        opkFrameView.layer.borderWidth = 2.0

        let captureDevice = AVCaptureDevice.default(for: AVMediaType.video)
        do {
            let input = try AVCaptureDeviceInput(device: captureDevice!)
            captureSession = AVCaptureSession()
            captureSession?.addInput(input)

            videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
            videoPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
            videoPreviewLayer?.frame = previewView.layer.bounds
            previewView.layer.addSublayer(videoPreviewLayer!)
            let captureOutput = AVCaptureVideoDataOutput()
            captureSession?.addOutput(captureOutput)
            captureOutput.setSampleBufferDelegate(self as! AVCaptureVideoDataOutputSampleBufferDelegate, queue: DispatchQueue.main)
            let conn = captureOutput.connection(with: AVMediaType.video)
            conn?.videoOrientation = AVCaptureVideoOrientation.portrait
            captureSession?.startRunning()
        } catch {
            print(error)
        }

        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

extension ViewController : AVCaptureVideoDataOutputSampleBufferDelegate {
    func plot(a: [CGFloat], b: [[String: CGFloat]], c: [CGFloat], min: CGFloat, max: CGFloat) {
        for sublayer in plotView.layer.sublayers ?? [] {
            sublayer.removeFromSuperlayer()
        }
        let line = CAShapeLayer()
        let linePath = UIBezierPath()
        linePath.move(to: CGPoint(x: 0, y: 0))
        for (idx, p) in a.enumerated() {
            linePath.addLine(to: CGPoint(x: CGFloat(idx), y: 100 * p / (max - min) + min))
        }
        linePath.addLine(to: CGPoint(x: 250, y: 0))
        line.path = linePath.cgPath
        line.strokeColor = UIColor.red.cgColor
        line.fillColor = UIColor.clear.cgColor
        line.lineWidth = 1

        let line2 = CAShapeLayer()
        let linePath2 = UIBezierPath()
        linePath2.move(to: CGPoint(x: 0, y: 0))
        for l in b {
            linePath2.addLine(to: CGPoint(x: l["start"]!, y: 0))
            linePath2.addLine(to: CGPoint(x: l["start"]!, y: 40))
            linePath2.addLine(to: CGPoint(x: l["end"]!, y: 40))
            linePath2.addLine(to: CGPoint(x: l["end"]!, y: 0))
        }
        linePath2.addLine(to: CGPoint(x: 250, y: 0))
        line2.path = linePath2.cgPath
        line2.strokeColor = UIColor.blue.cgColor
        line2.fillColor = UIColor.clear.cgColor
        line2.lineWidth = 1

        let line3 = CAShapeLayer()
        let linePath3 = UIBezierPath()
        linePath3.move(to: CGPoint(x: 0, y: 0))
        for (idx, p) in c.enumerated() {
            linePath3.addLine(to: CGPoint(x: CGFloat(idx), y: 100 * p / (max - min) + min))
        }
        linePath3.addLine(to: CGPoint(x: 250, y: 0))
        line3.path = linePath3.cgPath
        line3.strokeColor = UIColor.green.cgColor
        line3.fillColor = UIColor.clear.cgColor
        line3.lineWidth = 1
        plotView.layer.addSublayer(line)
        plotView.layer.addSublayer(line2)
        plotView.layer.addSublayer(line3)
    }

    func convertImageToGrayScale(image: UIImage) -> UIImage {
        // Create image rectangle with current image width/height
        let imageRect: CGRect = CGRect(x: 0, y: 0, width: image.size.width, height: image.size.height)

        // Grayscale color space
        let colorSpace: CGColorSpace = CGColorSpaceCreateDeviceGray()

        // Create bitmap content with current image size and grayscale colorspace
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.none.rawValue)
        let context = CGContext(data: nil, width: Int(image.size.width), height: Int(image.size.height), bitsPerComponent: 8, bytesPerRow: 0, space: colorSpace, bitmapInfo: bitmapInfo.rawValue)!

        // Draw image into current context, with specified rectangle using previously defined context (with grayscale colorspace)
        context.draw(image.cgImage!, in: imageRect)

        // Create bitmap image info from pixel data in current context
        let imageRef: CGImage = context.makeImage()!

        // Create a new UIImage object
        let newImage: UIImage = UIImage(cgImage: imageRef)

        // Return the new grayscale image
        return newImage
    }

    func grayscaleImageIntensity(image: UIImage) -> [UInt8] {
        // Create image rectangle with current image width/height
        let imageRect: CGRect = CGRect(x: 0, y: 0, width: image.size.width, height: image.size.height)

        // Grayscale color space
        let colorSpace: CGColorSpace = CGColorSpaceCreateDeviceGray()

        // Create bitmap content with current image size and grayscale colorspace
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.none.rawValue)
        var intensities = [UInt8](repeating: 0, count: Int(image.size.width * image.size.height))
        let context = CGContext(data: &intensities, width: Int(image.size.width), height: Int(image.size.height), bitsPerComponent: 8, bytesPerRow: Int(image.size.width), space: colorSpace, bitmapInfo: bitmapInfo.rawValue)!

        // Draw image into current context, with specified rectangle using previously defined context (with grayscale colorspace)
        context.draw(image.cgImage!, in: imageRect)

        // Return the new grayscale image
        return intensities
    }

    func captureOutput(_ output: AVCaptureOutput,
                  didOutput sampleBuffer: CMSampleBuffer,
                       from connection: AVCaptureConnection) {
        let h = 100;
        let w = 250;
        let imageBuffer: CVPixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer)!
        let ciimage : CIImage = CIImage(cvPixelBuffer: imageBuffer)
        let context : CIContext = CIContext(options: nil)
        let myImage : CGImage = context.createCGImage(
            ciimage, from: CGRect(x: ciimage.extent.midX - CGFloat(w), y: ciimage.extent.midY - CGFloat(h),
            width: CGFloat(w) * 2, height: CGFloat(h) * 2))!
        var uiimage : UIImage = UIImage(cgImage: myImage)

        UIGraphicsBeginImageContextWithOptions(
            CGSize(width: w, height: h), false, 1)
        uiimage.draw(in: CGRect(x: 0, y: 0, width: w, height: h))
        uiimage = UIGraphicsGetImageFromCurrentImageContext()!
        UIGraphicsEndImageContext()

//        let extractedGrayUiImage = self.convertImageToGrayScale(image: uiimage)
//        searchArea.image = extractedGrayUiImage
        searchArea.image = uiimage

        let grayCopy = uiimage

        if self.intervalCtrl % 2 == 0 {
            let intensities = self.grayscaleImageIntensity(image: grayCopy)
            let cLineLR = LineDetector.cLineLeftRight(pixels: intensities, w: w)
            if cLineLR["rc"] as! Int == 0 {
                cLineOverlay.isHidden = false
                cLineOverlay.frame = CGRect(
                x: searchArea.frame.origin.x + CGFloat(cLineLR["start"] as! Int),
                y: searchArea.frame.origin.y,
                width: CGFloat(cLineLR["end"] as! Int) - CGFloat(cLineLR["start"] as! Int), height: CGFloat(100))
            } else {
                cLineOverlay.isHidden = true
            }
            if let isLine = cLineLR["isLine"] as? [CGFloat] {
                plot(a: isLine, b: cLineLR["lines"] as! [[String: CGFloat]],
                    c: cLineLR["std"] as! [CGFloat], min: -1.5, max: 1.5)
            }
        }
        self.intervalCtrl = self.intervalCtrl + 1
        self.intervalCtrl = self.intervalCtrl % 64000

        // Recognized
//        let pixelData = ((extractedGrayUiImage.cgImage?.dataProvider)!).data
//        var data: UnsafePointer<UInt8> = CFDataGetBytePtr(pixelData)
//        print(data[h * w])
//        print(data[1])
//        print(data[2])
//
//        var cR : CGFloat = 0.0, cG : CGFloat = 0.0, cB : CGFloat = 0.0;
//        /*var cRCnt = 0, cGCnt = 0, cBCnt = 0;
//
//        for y in 5 ..< h - 5 // Height of your Pixture
//        {
//            for x in 187 ..< 187 + 24 // Width of your Picture
//            {
//                var pixelInfo: Int = ((Int(extractedGrayUiImage.size.width) * y) + x) * 4
//                var r = CGFloat(data[pixelInfo])
//                var g = CGFloat(data[pixelInfo+1])
//                var b = CGFloat(data[pixelInfo+2])
//                cR += r;
//                cRCnt += 1;
//                cG += g;
//                cGCnt += 1;
//                cB += b;
//                cBCnt += 1;
//            }
//        }
//        cR /= CGFloat(cRCnt)
//        cG /= CGFloat(cGCnt)
//        cB /= CGFloat(cBCnt) */
////        var pixelInfo: Int = (Int(extractedGrayUiImage.size.width) * 16 + 91) * 4
//        var pixelInfo: Int = (Int(extractedGrayUiImage.size.width * 16 + 91) * 4)
//        cR = CGFloat(data[pixelInfo+2])
//        cG = CGFloat(data[pixelInfo+1])
//        cB = CGFloat(data[pixelInfo])
//
//
//        // Draw recognized
//        let threshold : Float = 10.0
//        let threshold2 : Float = 15.0
//        var pixelArray: [m_RGBColor] = [m_RGBColor]()
//        var pixelColor: m_RGBColor = m_RGBColor()
//        var pixelArray2: [m_RGBColor] = [m_RGBColor]()
//        var pixelColor2: m_RGBColor = m_RGBColor()
//        var hitScore : Float = 0.0
//        for y in 0 ..< 32 // Height of your Pixture
//        {
//            for x in 0 ..< 128 // Width of your Picture
//            {
//
////                var onePixel = m_RGBColor()
////                var pixelInfo: Int = ((Int(extractedGrayUiImage.size.width) * y) + x) * 4
////                onePixel.Red   = UInt8(r) // Fill one Pixel with your Picture Data
////                onePixel.Green = UInt8(g) // Fill one Pixel with your Picture Data
////                onePixel.Blue  = UInt8(b) // Fill one Pixel with your Picture Data
////                pixelArray.append(onePixel)
////                continue
//                var onePixel = m_RGBColor()
//                var onePixel2 = m_RGBColor()
//                var pixelInfo: Int = ((Int(extractedGrayUiImage.size.width) * y) + x) * 4
//                var r = CGFloat(data[pixelInfo+2])
//                var g = CGFloat(data[pixelInfo+1])
//                var b = CGFloat(data[pixelInfo+0])
//                if sqrtf(Float((cR - r) * (cR - r) + (cG - g) * (cG - g) + (cB - b) * (cB - b))) <= threshold {
//                    onePixel.Red   = UInt8(r) // Fill one Pixel with your Picture Data
//                    onePixel.Green = UInt8(g) // Fill one Pixel with your Picture Data
//                    onePixel.Blue  = UInt8(b) // Fill one Pixel with your Picture Data
//
//                    if x >= 85 && x <= 85 + 12 {
//                        hitScore += 1.0
//                    } else if x > 85 - 12 && x < 85 + 12 + 12 {
//                        hitScore -= 4.0
//                    }
//                }
//                else {
//                    onePixel.Red   = 255 // Fill one Pixel with your Picture Data
//                    onePixel.Green = 255 // Fill one Pixel with your Picture Data
//                    onePixel.Blue  = 255 // Fill one Pixel with your Picture Data
//                }
//                pixelArray.append(onePixel)
//                if sqrtf(Float((cR - r) * (cR - r) + (cG - g) * (cG - g) + (cB - b) * (cB - b))) <= threshold2 {
//                    onePixel2.Red   = UInt8(r) // Fill one Pixel with your Picture Data
//                    onePixel2.Green = UInt8(g) // Fill one Pixel with your Picture Data
//                    onePixel2.Blue  = UInt8(b) // Fill one Pixel with your Picture Data
//                }
//                else {
//                    onePixel2.Red   = 255 // Fill one Pixel with your Picture Data
//                    onePixel2.Green = 255 // Fill one Pixel with your Picture Data
//                    onePixel2.Blue  = 255 // Fill one Pixel with your Picture Data
//                }
//                pixelArray2.append(onePixel2)
//            }
//        }
//        let bitmapCount: Int = pixelArray.count
//        let elmentLength: Int = MemoryLayout<m_RGBColor>.size
//        let render: CGColorRenderingIntent = CGColorRenderingIntent.defaultIntent
//        let rgbColorSpace = CGColorSpaceCreateDeviceRGB()
//        let bitmapInfo: CGBitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedFirst.rawValue)
//        let providerRef: CGDataProvider? = CGDataProvider(data:
//            NSData(bytes: &pixelArray, length: bitmapCount * elmentLength))
//        let cgimage: CGImage? = CGImage(width: 128, height: 32,
//            bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: 128 * elmentLength,
//            space: rgbColorSpace, bitmapInfo: bitmapInfo, provider: providerRef!,
//            decode: nil, shouldInterpolate: true, intent: render)
//        if cgimage != nil
//        {
//            // You have success, the Image is valid and usable
//            recognizedImage.image = UIImage(cgImage: cgimage!)
//        }
//
//        let providerRef2: CGDataProvider? = CGDataProvider(data:
//            NSData(bytes: &pixelArray2, length: bitmapCount * elmentLength))
//        let cgimage2: CGImage? = CGImage(width: 128, height: 32,
//            bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: 128 * elmentLength,
//            space: rgbColorSpace, bitmapInfo: bitmapInfo, provider: providerRef2!,
//            decode: nil, shouldInterpolate: true, intent: render)
//        if cgimage2 != nil
//        {
//            // You have success, the Image is valid and usable
//            recognizedImage2.image = UIImage(cgImage: cgimage2!)
//        }
//        if hitScore > 40 {
//            resultC.backgroundColor = UIColor(red: cR / 255, green: cG / 255, blue: cB / 255, alpha: 1)
//            print("Hit sampled C color r: \(cR), g: \(cG), b: \(cB), ")
//        } else {
//            resultC.backgroundColor = UIColor.white
//        }
    }
}

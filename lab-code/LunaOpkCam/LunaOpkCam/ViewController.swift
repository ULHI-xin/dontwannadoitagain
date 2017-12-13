//
//  ViewController.swift
//  LunaOpkCam
//
//  Created by 欣 赵 on 21/11/2017.
//  Copyright © 2017 ZX. All rights reserved.
//
import AVFoundation
import UIKit

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
}

class ViewController: UIViewController {
    var captureSession: AVCaptureSession?
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    @IBOutlet weak var previewView: UIView!
    @IBOutlet weak var searchArea: UIImageView!
    @IBOutlet weak var recognizedImage2: UIImageView!
    @IBOutlet weak var recognizedImage: UIImageView!
    @IBOutlet weak var opkFrameView: UIView!
    @IBOutlet weak var resultC: UIView!
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
        print("median")
        print(LnMath.median(a: LnMath.stdX(a: s, w: 10, h: 4)))
        print("medianX")
        print(LnMath.medianX(a: s, w: 10, h: 4))

        let scnb = Scanable(pixels: s, w: 10)
        print("scnb.stdMean")
        print(scnb.stdMean)
        print("scnb.diff")
        print(scnb.diff)
        print("scnb.std")
        print(scnb.std)
        print("scnb.stdVar")
        print(scnb.stdVar)

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

        let extractedGrayUiImage = self.convertImageToGrayScale(image: uiimage)
        searchArea.image = extractedGrayUiImage

//        let intensities: [CGFloat] = self.grayscaleImageIntensity(image: extractedGrayUiImage) as [CGFloat]
//        let scanable = Scanable(pixels: intensities, w: 250)

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

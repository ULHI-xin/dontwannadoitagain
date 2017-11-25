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

class ViewController: UIViewController {
    var captureSession: AVCaptureSession?
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    @IBOutlet weak var previewView: UIView!
    @IBOutlet weak var extractedImage: UIImageView!
    @IBOutlet weak var recognizedImage2: UIImageView!
    @IBOutlet weak var recognizedImage: UIImageView!
    @IBOutlet weak var opkFrameView: UIView!
    @IBOutlet weak var resultC: UIView!
    override func viewDidLoad() {
        super.viewDidLoad()

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
    func captureOutput(_ output: AVCaptureOutput,
                  didOutput sampleBuffer: CMSampleBuffer,
                       from connection: AVCaptureConnection) {
//        print(sampleBuffer);
        let h = 32 * 2;
        let w = 128 * 2;
        let sw = 12 * 2;
        let imageBuffer: CVPixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer)!
//        print("imageBuffer")
//        print(imageBuffer)
        let ciimage : CIImage = CIImage(cvPixelBuffer: imageBuffer)
//        print("ciimage")
//        print(ciimage)
        let context : CIContext = CIContext(options: nil)
        let myImage : CGImage = context.createCGImage(
            ciimage, from: CGRect(x: ciimage.extent.midX - CGFloat(w) / 2, y: ciimage.extent.midY - CGFloat(h) / 2,
            width: CGFloat(w), height: CGFloat(h)))!
//        print("myimage")
//        print(myImage)
        var uiimage : UIImage = UIImage(cgImage: myImage)

        UIGraphicsBeginImageContextWithOptions(
            CGSize(width: 128, height: 32), false, 1)
        uiimage.draw(in: CGRect(x: 0, y: 0, width: 128, height: 32))
        uiimage = UIGraphicsGetImageFromCurrentImageContext()!
        UIGraphicsEndImageContext()

//        // CIFilter to grayscale
//        let currentFilter = CIFilter(name: "CIPhotoEffectNoir")
//        currentFilter!.setValue(CIImage(image: uiimage), forKey: kCIInputImageKey)
//        let output = currentFilter!.outputImage
//        let cgimg = context.createCGImage(output!, from: output!.extent)
//        let extractedGrayUiImage = UIImage(cgImage: cgimg!)
//        print("extractedGrayUiImage")
//        print(extractedGrayUiImage)

//        print(extractedGrayUiImage.cgImage)
        let extractedGrayUiImage = uiimage
        extractedImage.image = extractedGrayUiImage;

        // Recognized
        let pixelData = ((extractedGrayUiImage.cgImage?.dataProvider)!).data
        var data: UnsafePointer<UInt8> = CFDataGetBytePtr(pixelData)

        var cR : CGFloat = 0.0, cG : CGFloat = 0.0, cB : CGFloat = 0.0;
        /*var cRCnt = 0, cGCnt = 0, cBCnt = 0;

        for y in 5 ..< h - 5 // Height of your Pixture
        {
            for x in 187 ..< 187 + 24 // Width of your Picture
            {
                var pixelInfo: Int = ((Int(extractedGrayUiImage.size.width) * y) + x) * 4
                var r = CGFloat(data[pixelInfo])
                var g = CGFloat(data[pixelInfo+1])
                var b = CGFloat(data[pixelInfo+2])
                cR += r;
                cRCnt += 1;
                cG += g;
                cGCnt += 1;
                cB += b;
                cBCnt += 1;
            }
        }
        cR /= CGFloat(cRCnt)
        cG /= CGFloat(cGCnt)
        cB /= CGFloat(cBCnt) */
//        var pixelInfo: Int = (Int(extractedGrayUiImage.size.width) * 16 + 91) * 4
        var pixelInfo: Int = (Int(extractedGrayUiImage.size.width * 16 + 91) * 4)
        cR = CGFloat(data[pixelInfo+2])
        cG = CGFloat(data[pixelInfo+1])
        cB = CGFloat(data[pixelInfo])


        // Draw recognized
        let threshold : Float = 10.0
        let threshold2 : Float = 15.0
        var pixelArray: [m_RGBColor] = [m_RGBColor]()
        var pixelColor: m_RGBColor = m_RGBColor()
        var pixelArray2: [m_RGBColor] = [m_RGBColor]()
        var pixelColor2: m_RGBColor = m_RGBColor()
        var hitScore : Float = 0.0
        for y in 0 ..< 32 // Height of your Pixture
        {
            for x in 0 ..< 128 // Width of your Picture
            {

//                var onePixel = m_RGBColor()
//                var pixelInfo: Int = ((Int(extractedGrayUiImage.size.width) * y) + x) * 4
//                onePixel.Red   = UInt8(r) // Fill one Pixel with your Picture Data
//                onePixel.Green = UInt8(g) // Fill one Pixel with your Picture Data
//                onePixel.Blue  = UInt8(b) // Fill one Pixel with your Picture Data
//                pixelArray.append(onePixel)
//                continue
                var onePixel = m_RGBColor()
                var onePixel2 = m_RGBColor()
                var pixelInfo: Int = ((Int(extractedGrayUiImage.size.width) * y) + x) * 4
                var r = CGFloat(data[pixelInfo+2])
                var g = CGFloat(data[pixelInfo+1])
                var b = CGFloat(data[pixelInfo+0])
                if sqrtf(Float((cR - r) * (cR - r) + (cG - g) * (cG - g) + (cB - b) * (cB - b))) <= threshold {
                    onePixel.Red   = UInt8(r) // Fill one Pixel with your Picture Data
                    onePixel.Green = UInt8(g) // Fill one Pixel with your Picture Data
                    onePixel.Blue  = UInt8(b) // Fill one Pixel with your Picture Data

                    if x >= 85 && x <= 85 + 12 {
                        hitScore += 1.0
                    } else if x > 85 - 12 && x < 85 + 12 + 12 {
                        hitScore -= 4.0
                    }
                }
                else {
                    onePixel.Red   = 255 // Fill one Pixel with your Picture Data
                    onePixel.Green = 255 // Fill one Pixel with your Picture Data
                    onePixel.Blue  = 255 // Fill one Pixel with your Picture Data
                }
                pixelArray.append(onePixel)
                if sqrtf(Float((cR - r) * (cR - r) + (cG - g) * (cG - g) + (cB - b) * (cB - b))) <= threshold2 {
                    onePixel2.Red   = UInt8(r) // Fill one Pixel with your Picture Data
                    onePixel2.Green = UInt8(g) // Fill one Pixel with your Picture Data
                    onePixel2.Blue  = UInt8(b) // Fill one Pixel with your Picture Data
                }
                else {
                    onePixel2.Red   = 255 // Fill one Pixel with your Picture Data
                    onePixel2.Green = 255 // Fill one Pixel with your Picture Data
                    onePixel2.Blue  = 255 // Fill one Pixel with your Picture Data
                }
                pixelArray2.append(onePixel2)
            }
        }
        let bitmapCount: Int = pixelArray.count
        let elmentLength: Int = MemoryLayout<m_RGBColor>.size
        let render: CGColorRenderingIntent = CGColorRenderingIntent.defaultIntent
        let rgbColorSpace = CGColorSpaceCreateDeviceRGB()
        let bitmapInfo: CGBitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedFirst.rawValue)
        let providerRef: CGDataProvider? = CGDataProvider(data:
            NSData(bytes: &pixelArray, length: bitmapCount * elmentLength))
        let cgimage: CGImage? = CGImage(width: 128, height: 32,
            bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: 128 * elmentLength,
            space: rgbColorSpace, bitmapInfo: bitmapInfo, provider: providerRef!,
            decode: nil, shouldInterpolate: true, intent: render)
        if cgimage != nil
        {
            // You have success, the Image is valid and usable
            recognizedImage.image = UIImage(cgImage: cgimage!)
        }

        let providerRef2: CGDataProvider? = CGDataProvider(data:
            NSData(bytes: &pixelArray2, length: bitmapCount * elmentLength))
        let cgimage2: CGImage? = CGImage(width: 128, height: 32,
            bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: 128 * elmentLength,
            space: rgbColorSpace, bitmapInfo: bitmapInfo, provider: providerRef2!,
            decode: nil, shouldInterpolate: true, intent: render)
        if cgimage2 != nil
        {
            // You have success, the Image is valid and usable
            recognizedImage2.image = UIImage(cgImage: cgimage2!)
        }
        if hitScore > 40 {
            resultC.backgroundColor = UIColor(red: cR / 255, green: cG / 255, blue: cB / 255, alpha: 1)
            print("Hit sampled C color r: \(cR), g: \(cG), b: \(cB), ")
        } else {
            resultC.backgroundColor = UIColor.white
        }
    }
}

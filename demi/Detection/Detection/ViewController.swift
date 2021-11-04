//
//  ViewController.swift
//  Detection
//
//  Created by Demi, Tao Yiwei on 04/11/2021.
//  Copyright © 2021 Demi, Tao Yiwei. All rights reserved.
//

import UIKit
import AVKit
import AVFoundation


class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    @IBOutlet weak var recordButton: UIButton!
    @IBOutlet weak var recordPreview: UIImageView!
    
    @IBOutlet weak var photoLibraryButton: UIButton!
    @IBOutlet weak var photoLibraryPreview: UIImageView!
    
    @IBAction func playVideo(_ sender: AnyObject) {
        guard let url = URL(string: "https://www.youtube.com/watch?v=2_N3VDK_dJQ") else {
            return
        }
        let player = AVPlayer(url: url)
        
        let controller = AVPlayerViewController()
        controller.player = player
        
        present(controller, animated: true) {
            player.play()
        }
    }
    
    let captureSession = AVCaptureSession()
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    let videoDataOutput = AVCaptureVideoDataOutput()
    let videoDataOutputQueue = DispatchQueue(label: "VideoDataOutput", qos: .userInitiated, attributes: [], autoreleaseFrequency: .workItem)
    var videoFrameSzie: CGSize = .zero
    
    // Get the first available camera for input device
    var deviceInput: AVCaptureDeviceInput!
    let videoDevice = AVCaptureDevice.DiscoverySession(deviceTypes: [.builtInWideAngleCamera], mediaType: .video, position: .back).devices.first
    
    
    // do something: data in the queue send to the server

    
    // receive from server
    
    // put a layer on top of previewlayer
    
    public func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        // We will handle frame(s) here
    }
    
    public func captureOutput(_ captureOutput: AVCaptureOutput, didDrop didDropSampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        // Dropped frame(s) can be handled here
    }
    
    public func startCapture() {
        if !captureSession.isRunning {
            captureSession.startRunning()
        }
    }
    
    // referecne: https://blog.csdn.net/mzl87/article/details/116212500
    // need to study: Dispatch Queue + custome layer
    
    
    
    
    
    
    
   

}

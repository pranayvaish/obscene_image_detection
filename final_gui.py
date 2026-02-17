import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from tensorflow import keras
import shutil
import os
from datetime import datetime

class ImageUploadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Image Upload System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.selected_image_path = None
        self.model = None
        self.upload_folder = "uploaded_images"  # Folder where approved images will be saved
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
        
        # Title
        title_frame = tk.Frame(root, bg="#2c3e50", pady=20)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="Safe Image Upload System",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Only SFW images will be uploaded • No preview for safety",
            font=("Helvetica", 12),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content area
        content_frame = tk.Frame(root, bg="#f0f0f0", pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Selected file info area
        info_frame = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, bd=2, pady=30)
        info_frame.pack(pady=20, fill=tk.X)
        
        self.file_info_label = tk.Label(
            info_frame,
            text="No image selected",
            font=("Helvetica", 14),
            bg="white",
            fg="#7f8c8d",
            wraplength=600
        )
        self.file_info_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Select Image button
        select_btn = tk.Button(
            button_frame,
            text="📁 Select Image",
            command=self.select_image,
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            cursor="hand2",
            padx=40,
            pady=15,
            relief=tk.FLAT
        )
        select_btn.pack(side=tk.LEFT, padx=10)
        
        # Upload button
        self.upload_btn = tk.Button(
            button_frame,
            text="⬆️ Upload Image",
            command=self.upload_image,
            font=("Helvetica", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            cursor="hand2",
            padx=40,
            pady=15,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.upload_btn.pack(side=tk.LEFT, padx=10)
        
        # Status frame
        self.status_frame = tk.Frame(content_frame, bg="#ecf0f1", relief=tk.RIDGE, bd=2)
        self.status_frame.pack(pady=30, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Status: Waiting for image selection...",
            font=("Helvetica", 13),
            bg="#ecf0f1",
            fg="#34495e",
            pady=25,
            wraplength=700
        )
        self.status_label.pack()
        
        # Upload history frame
        history_label = tk.Label(
            content_frame,
            text="Upload History",
            font=("Helvetica", 14, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        history_label.pack(anchor=tk.W, pady=(10, 5))
        
        history_frame = tk.Frame(content_frame, bg="white", relief=tk.RIDGE, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for history
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(
            history_frame,
            font=("Courier", 10),
            bg="white",
            fg="#2c3e50",
            yscrollcommand=scrollbar.set,
            height=8,
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.history_text.yview)
        
        # Load model
        self.load_model()
    
    def load_model(self):
        """
        Load your trained TensorFlow/Keras model.
        """
        try:
            # ========== ADD YOUR MODEL PATH HERE ==========
            MODEL_PATH = r"C:\Users\hp\Desktop\Project Cdac\obscene_image_detection\cnn_obscene_detect.keras"
            # ==============================================
            
            self.model = keras.models.load_model(MODEL_PATH)
            print("✅ Model loaded successfully!")
            self.add_to_history("✅ System Ready - Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Failed to load model: {str(e)}")
            messagebox.showerror("Error", f"Failed to load model: {str(e)}\n\nPlease check the MODEL_PATH.")
            self.model = None
            self.add_to_history("❌ ERROR - Failed to load model")
    
    def select_image(self):
        """Open file dialog to select an image"""
        file_path = filedialog.askopenfilename(
            title="Select an image to upload",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_image_path = file_path
            filename = os.path.basename(file_path)
            
            # Show only filename, no preview
            self.file_info_label.config(
                text=f"Selected: {filename}\n\nClick 'Upload Image' to verify and upload",
                fg="#2c3e50"
            )
            
            self.upload_btn.config(state=tk.NORMAL)
            self.status_label.config(
                text="Status: Image selected - Click 'Upload Image' to verify content and upload",
                bg="#3498db",
                fg="white"
            )
    
    def preprocess_image(self, image_path):
        """
        Preprocess the image for your TensorFlow model.
        """
        try:
            # Open image
            image = Image.open(image_path)
            
            # ========== ADJUST THESE PARAMETERS ==========
            TARGET_SIZE = (224, 224)  # Change to match your model's input size
            
            image = image.resize(TARGET_SIZE)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Normalize (0-1 scaling)
            image_array = image_array.astype('float32') / 255.0
            # ==============================================
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            raise Exception(f"Preprocessing failed: {str(e)}")
    
    def check_image_safety(self, image_path):
        """
        Check if image is SFW using the model.
        Returns: (is_safe, nsfw_confidence, sfw_confidence)
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Make prediction
            prediction = self.model.predict(processed_image, verbose=0)
            raw_output = float(prediction[0][0])
            
            # ========== CONFIGURE YOUR MODEL'S OUTPUT INTERPRETATION ==========
            # CHOOSE ONE OF THE FOLLOWING OPTIONS:
            
            # OPTION 1: Model outputs NSFW probability (high value = NSFW)
            # Uncomment the lines below if your model works this way:
            # nsfw_confidence = raw_output
            # sfw_confidence = 1 - raw_output
            # is_nsfw = nsfw_confidence > 0.5
            
            # OPTION 2: Model outputs SFW probability (high value = SFW) - LIKELY YOUR CASE
            # Uncomment the lines below if your model works this way:
            sfw_confidence = raw_output
            nsfw_confidence = 1 - raw_output
            is_nsfw = sfw_confidence < 0.5  # If SFW confidence is low, it's NSFW
            
            # ==================================================================
            
            is_safe = not is_nsfw
            
            return is_safe, nsfw_confidence, sfw_confidence
            
        except Exception as e:
            raise Exception(f"Safety check failed: {str(e)}")
    
    def upload_image(self):
        """Upload image after checking if it's SFW"""
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        if self.model is None:
            messagebox.showerror("Error", "Model not loaded. Cannot verify image safety.")
            return
        
        try:
            # Update status - checking
            self.status_label.config(
                text="Status: Verifying image content... Please wait...",
                bg="#f39c12",
                fg="white"
            )
            self.root.update()
            
            # Check if image is safe
            is_safe, nsfw_confidence, sfw_confidence = self.check_image_safety(self.selected_image_path)
            
            if is_safe:
                # Image is SFW - proceed with upload
                self.perform_upload(sfw_confidence, nsfw_confidence)
            else:
                # Image is NSFW - reject upload
                self.reject_upload(nsfw_confidence, sfw_confidence)
                
        except Exception as e:
            messagebox.showerror("Error", f"Upload failed: {str(e)}")
            self.status_label.config(
                text="Status: Upload failed - Error occurred",
                bg="#e74c3c",
                fg="white"
            )
    
    def perform_upload(self, sfw_confidence, nsfw_confidence):
        """Actually upload the image (save to upload folder)"""
        try:
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = os.path.basename(self.selected_image_path)
            name, ext = os.path.splitext(original_filename)
            new_filename = f"{name}_{timestamp}{ext}"
            
            destination = os.path.join(self.upload_folder, new_filename)
            
            # Copy image to upload folder
            shutil.copy2(self.selected_image_path, destination)
            
            # Show success message
            sfw_percent = sfw_confidence * 100
            
            self.status_label.config(
                text=f"✅ SUCCESS - Image uploaded! (SFW Confidence: {sfw_percent:.1f}%)",
                bg="#27ae60",
                fg="white",
                font=("Helvetica", 13, "bold")
            )
            
            # Add to history
            self.add_to_history(f"✅ UPLOADED: {original_filename} → {new_filename} (SFW: {sfw_percent:.1f}%)")
            
            # Show success dialog
            messagebox.showinfo(
                "Upload Successful",
                f"Image uploaded successfully!\n\n"
                f"Original: {original_filename}\n"
                f"Saved as: {new_filename}\n"
                f"Location: {self.upload_folder}\n\n"
                f"SFW Confidence: {sfw_percent:.1f}%"
            )
            
            # Reset for next upload
            self.reset_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def reject_upload(self, nsfw_confidence, sfw_confidence):
        """Reject NSFW image upload"""
        nsfw_percent = nsfw_confidence * 100
        
        self.status_label.config(
            text=f"❌ UPLOAD BLOCKED - NSFW content detected (NSFW Confidence: {nsfw_percent:.1f}%)",
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 13, "bold")
        )
        
        # Add to history
        filename = os.path.basename(self.selected_image_path)
        self.add_to_history(f"❌ BLOCKED: {filename} - NSFW content (NSFW: {nsfw_percent:.1f}%)")
        
        # Show warning dialog
        messagebox.showwarning(
            "Upload Blocked",
            f"This image cannot be uploaded!\n\n"
            f"Reason: NSFW content detected\n"
            f"NSFW Confidence: {nsfw_percent:.1f}%\n\n"
            f"The image has not been saved.\n"
            f"Please select a different image."
        )
        
        # Reset and let user select different image
        self.reset_form()
    
    def reset_form(self):
        """Reset the form for next upload"""
        self.selected_image_path = None
        self.upload_btn.config(state=tk.DISABLED)
        
        self.file_info_label.config(
            text="No image selected",
            fg="#7f8c8d"
        )
        
        self.status_label.config(
            text="Status: Waiting for image selection...",
            bg="#ecf0f1",
            fg="#34495e",
            font=("Helvetica", 13)
        )
    
    def add_to_history(self, message):
        """Add message to upload history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ImageUploadGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
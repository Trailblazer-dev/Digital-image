import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing the digital_image package
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Check if tkinter and PIL.ImageTk are available
tkinter_available = True
pillow_tk_available = True
try:
    import tkinter as tk
    from tkinter import filedialog, ttk, messagebox
except ImportError:
    tkinter_available = False

try:
    from PIL import Image, ImageTk
except ImportError:
    pillow_tk_available = False

# Import CV2 and check it's available
cv2_available = True
try:
    import cv2
    from digital_image.basic_operations import load_image, convert_to_grayscale, save_image
    from digital_image.filters import (apply_gaussian_blur, apply_median_blur, 
                                      apply_bilateral_filter, apply_canny_edge_detector,
                                      apply_sobel_filter, apply_laplacian_filter)
    from digital_image.transformations import histogram_equalization, fourier_transform
    from digital_image.segmentation import (threshold_image, adaptive_threshold, 
                                          otsu_threshold, k_means_segmentation)
except ImportError as e:
    cv2_available = False
    print(f"Error importing required modules: {e}")
    print("Make sure you've installed all required packages")

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Image Processing")
        self.root.geometry("1200x800")
        
        # Set up the main frame structure
        self.setup_ui()
        
        # Initialize variables
        self.current_image = None
        self.original_image = None
        self.filename = None
        self.processing_history = []
        
        # Create output directory
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_images")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup_ui(self):
        # Create main frame for controls
        self.controls_frame = tk.Frame(self.root, width=300)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Create frame for image display
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add Load and Save buttons
        self.file_frame = tk.LabelFrame(self.controls_frame, text="File Operations")
        self.file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.load_btn = tk.Button(self.file_frame, text="Load Image", command=self.load_image)
        self.load_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_btn = tk.Button(self.file_frame, text="Save Image", command=self.save_image)
        self.save_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Add reset button
        self.reset_btn = tk.Button(self.controls_frame, text="Reset to Original", command=self.reset_to_original)
        self.reset_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Create notebook for organized operations
        self.notebook = ttk.Notebook(self.controls_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Basic operations tab
        self.basic_frame = tk.Frame(self.notebook)
        self.notebook.add(self.basic_frame, text="Basic")
        
        self.grayscale_btn = tk.Button(self.basic_frame, text="Convert to Grayscale", 
                                     command=self.convert_to_grayscale)
        self.grayscale_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Create rotation control with slider
        self.rotation_frame = tk.LabelFrame(self.basic_frame, text="Rotate Image")
        self.rotation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.rotation_slider = tk.Scale(self.rotation_frame, from_=0, to=360, 
                                      orient=tk.HORIZONTAL)
        self.rotation_slider.pack(fill=tk.X, padx=5)
        
        self.rotate_btn = tk.Button(self.rotation_frame, text="Apply Rotation", 
                                  command=self.rotate_image)
        self.rotate_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Create resize control
        self.resize_frame = tk.LabelFrame(self.basic_frame, text="Resize Image")
        self.resize_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.scale_label = tk.Label(self.resize_frame, text="Scale factor:")
        self.scale_label.pack(anchor=tk.W, padx=5)
        
        self.scale_entry = tk.Entry(self.resize_frame)
        self.scale_entry.insert(0, "0.5")
        self.scale_entry.pack(fill=tk.X, padx=5, pady=3)
        
        self.resize_btn = tk.Button(self.resize_frame, text="Apply Resize", 
                                  command=self.resize_image)
        self.resize_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Filters tab
        self.filters_frame = tk.Frame(self.notebook)
        self.notebook.add(self.filters_frame, text="Filters")
        
        # Gaussian blur
        self.gaussian_frame = tk.LabelFrame(self.filters_frame, text="Gaussian Blur")
        self.gaussian_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.gaussian_slider = tk.Scale(self.gaussian_frame, from_=1, to=25, 
                                      orient=tk.HORIZONTAL, label="Kernel Size")
        self.gaussian_slider.set(5)
        self.gaussian_slider.pack(fill=tk.X, padx=5)
        
        self.gaussian_btn = tk.Button(self.gaussian_frame, text="Apply Gaussian Blur", 
                                    command=self.apply_gaussian)
        self.gaussian_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Median blur
        self.median_btn = tk.Button(self.filters_frame, text="Apply Median Blur", 
                                   command=self.apply_median)
        self.median_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Bilateral filter
        self.bilateral_btn = tk.Button(self.filters_frame, text="Apply Bilateral Filter", 
                                      command=self.apply_bilateral)
        self.bilateral_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Edge detection
        self.edge_frame = tk.LabelFrame(self.filters_frame, text="Edge Detection")
        self.edge_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.canny_btn = tk.Button(self.edge_frame, text="Canny Edge Detection", 
                                 command=self.apply_canny)
        self.canny_btn.pack(fill=tk.X, padx=5, pady=3)
        
        self.sobel_btn = tk.Button(self.edge_frame, text="Sobel Filter", 
                                 command=self.apply_sobel)
        self.sobel_btn.pack(fill=tk.X, padx=5, pady=3)
        
        self.laplacian_btn = tk.Button(self.edge_frame, text="Laplacian Filter", 
                                     command=self.apply_laplacian)
        self.laplacian_btn.pack(fill=tk.X, padx=5, pady=3)
        
        # Transformations tab
        self.transform_frame = tk.Frame(self.notebook)
        self.notebook.add(self.transform_frame, text="Transform")
        
        self.hist_eq_btn = tk.Button(self.transform_frame, text="Histogram Equalization", 
                                   command=self.apply_histogram_eq)
        self.hist_eq_btn.pack(fill=tk.X, padx=5, pady=5)
        
        self.fourier_btn = tk.Button(self.transform_frame, text="Fourier Transform", 
                                   command=self.apply_fourier)
        self.fourier_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Segmentation tab
        self.segment_frame = tk.Frame(self.notebook)
        self.notebook.add(self.segment_frame, text="Segment")
        
        # Thresholding
        self.thresh_frame = tk.LabelFrame(self.segment_frame, text="Thresholding")
        self.thresh_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.thresh_slider = tk.Scale(self.thresh_frame, from_=0, to=255, 
                                    orient=tk.HORIZONTAL, label="Threshold Value")
        self.thresh_slider.set(127)
        self.thresh_slider.pack(fill=tk.X, padx=5)
        
        self.thresh_btn = tk.Button(self.thresh_frame, text="Apply Thresholding", 
                                  command=self.apply_threshold)
        self.thresh_btn.pack(fill=tk.X, padx=5, pady=5)
        
        self.adaptive_btn = tk.Button(self.segment_frame, text="Adaptive Thresholding", 
                                    command=self.apply_adaptive_threshold)
        self.adaptive_btn.pack(fill=tk.X, padx=5, pady=5)
        
        self.otsu_btn = tk.Button(self.segment_frame, text="Otsu Thresholding", 
                                command=self.apply_otsu)
        self.otsu_btn.pack(fill=tk.X, padx=5, pady=5)
        
        self.kmeans_btn = tk.Button(self.segment_frame, text="K-Means Segmentation", 
                                  command=self.apply_kmeans)
        self.kmeans_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Image display area with scrollbars
        self.canvas = tk.Canvas(self.image_frame, bg="lightgray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars for the canvas
        self.h_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, 
                                       command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, 
                                       command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, 
                              yscrollcommand=self.v_scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                 bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_image(self):
        self.filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        
        if not self.filename:
            return
        
        try:
            self.original_image = load_image(self.filename)
            if self.original_image is None:
                messagebox.showerror("Error", f"Could not load image: {self.filename}")
                return
            
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            self.processing_history = []
            self.status_var.set(f"Loaded: {os.path.basename(self.filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
    
    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        default_name = "processed_image.png"
        if self.filename:
            base_name = os.path.splitext(os.path.basename(self.filename))[0]
            default_name = f"{base_name}_processed.png"
        
        save_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("PNG files", "*.png"), 
                      ("JPEG files", "*.jpg"), 
                      ("All files", "*.*")]
        )
        
        if save_path:
            try:
                save_image(self.current_image, save_path)
                self.status_var.set(f"Image saved to: {os.path.basename(save_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {str(e)}")
    
    def display_image(self, image):
        # Convert OpenCV BGR to RGB for display
        if image is None:
            return
        
        if len(image.shape) == 3:
            display_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            # If grayscale, convert to 3-channel for proper display
            display_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Convert to PIL Image
        pil_img = Image.fromarray(display_image)
        
        # Convert PIL Image to PhotoImage
        self.photo = ImageTk.PhotoImage(pil_img)
        
        # Update canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
    def reset_to_original(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            self.status_var.set("Reset to original image")
    
    def convert_to_grayscale(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = convert_to_grayscale(self.current_image)
            self.display_image(self.current_image)
            self.status_var.set("Converted to grayscale")
        except Exception as e:
            messagebox.showerror("Error", f"Error converting to grayscale: {str(e)}")
    
    def rotate_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            angle = self.rotation_slider.get()
            from digital_image.basic_operations import rotate_image
            self.current_image = rotate_image(self.current_image, angle)
            self.display_image(self.current_image)
            self.status_var.set(f"Rotated by {angle} degrees")
        except Exception as e:
            messagebox.showerror("Error", f"Error rotating image: {str(e)}")
    
    def resize_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            scale = float(self.scale_entry.get())
            if scale <= 0:
                messagebox.showwarning("Warning", "Scale factor must be greater than 0")
                return
                
            from digital_image.basic_operations import resize_image
            self.current_image = resize_image(self.current_image, scale=scale)
            self.display_image(self.current_image)
            self.status_var.set(f"Resized with scale factor {scale}")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number for scale")
        except Exception as e:
            messagebox.showerror("Error", f"Error resizing image: {str(e)}")
    
    def apply_gaussian(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            ksize = self.gaussian_slider.get()
            # Make sure kernel size is odd
            if ksize % 2 == 0:
                ksize += 1
            
            self.current_image = apply_gaussian_blur(self.current_image, (ksize, ksize))
            self.display_image(self.current_image)
            self.status_var.set(f"Applied Gaussian blur with kernel size {ksize}")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Gaussian blur: {str(e)}")
    
    def apply_median(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = apply_median_blur(self.current_image, 5)
            self.display_image(self.current_image)
            self.status_var.set("Applied Median blur")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Median blur: {str(e)}")
    
    def apply_bilateral(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = apply_bilateral_filter(self.current_image)
            self.display_image(self.current_image)
            self.status_var.set("Applied Bilateral filter")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Bilateral filter: {str(e)}")
    
    def apply_canny(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            edges = apply_canny_edge_detector(self.current_image)
            # Convert to 3-channel for consistent display
            self.current_image = edges
            self.display_image(self.current_image)
            self.status_var.set("Applied Canny edge detection")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Canny edge detection: {str(e)}")
    
    def apply_sobel(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            sobel = apply_sobel_filter(self.current_image)
            # Normalize to 0-255 for display
            sobel_norm = cv2.normalize(sobel, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            self.current_image = sobel_norm
            self.display_image(self.current_image)
            self.status_var.set("Applied Sobel filter")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Sobel filter: {str(e)}")
    
    def apply_laplacian(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            laplacian = apply_laplacian_filter(self.current_image)
            # Normalize to 0-255 for display
            laplacian_norm = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            self.current_image = laplacian_norm
            self.display_image(self.current_image)
            self.status_var.set("Applied Laplacian filter")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Laplacian filter: {str(e)}")
    
    def apply_histogram_eq(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = histogram_equalization(self.current_image)
            self.display_image(self.current_image)
            self.status_var.set("Applied histogram equalization")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying histogram equalization: {str(e)}")
    
    def apply_fourier(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            _, _, magnitude_spectrum = fourier_transform(self.current_image)
            # Normalize to 0-255 for display
            magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            self.current_image = magnitude_spectrum
            self.display_image(self.current_image)
            self.status_var.set("Applied Fourier transform (magnitude spectrum)")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Fourier transform: {str(e)}")
    
    def apply_threshold(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            threshold_value = self.thresh_slider.get()
            self.current_image = threshold_image(self.current_image, threshold_value)
            self.display_image(self.current_image)
            self.status_var.set(f"Applied thresholding with value {threshold_value}")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying thresholding: {str(e)}")
    
    def apply_adaptive_threshold(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = adaptive_threshold(self.current_image)
            self.display_image(self.current_image)
            self.status_var.set("Applied adaptive thresholding")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying adaptive thresholding: {str(e)}")
    
    def apply_otsu(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = otsu_threshold(self.current_image)
            self.display_image(self.current_image)
            self.status_var.set("Applied Otsu thresholding")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying Otsu thresholding: {str(e)}")
    
    def apply_kmeans(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            self.current_image = k_means_segmentation(self.current_image, k=3)
            self.display_image(self.current_image)
            self.status_var.set("Applied K-means segmentation")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying K-means segmentation: {str(e)}")


def main():
    """Main function to run the GUI application or provide alternatives"""
    # Check if all required components are available
    if not tkinter_available:
        print("Error: Tkinter is not available on your system.")
        print("Tkinter is required for the GUI interface.")
        print("\nInstall Tkinter through your system package manager:")
        print("- Ubuntu/Debian: sudo apt-get install python3-tk")
        print("- Fedora: sudo dnf install python3-tkinter")
        print("- macOS with Homebrew: brew install python-tk")
        return 1
    
    if not pillow_tk_available:
        print("Error: PIL.ImageTk is not available.")
        print("This component is required for displaying images in the GUI.")
        print("\nTry reinstalling Pillow with Tkinter support:")
        print("- Ubuntu/Debian: sudo apt-get install python3-pil.imagetk")
        print("- With pip: pip uninstall Pillow && pip install --upgrade Pillow")
        return 1
    
    if not cv2_available:
        print("Error: OpenCV (cv2) is not properly installed.")
        print("Install it with: pip install opencv-python")
        return 1
    
    try:
        root = tk.Tk()
        app = ImageProcessingApp(root)
        root.mainloop()
        return 0
    except Exception as e:
        print(f"Error starting the GUI application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

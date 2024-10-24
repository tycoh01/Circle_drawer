import 'dart:html';

// Function to convert centimeters to pixels (assuming screen DPI is 96)
double cmToPx(double cm) {
  const double dpi = 96;  // Standard DPI for web screens
  return (cm / 2.54) * dpi;  // 1 inch = 2.54 cm
}

void main() {
  // Query the canvas element from the HTML page by its ID
  CanvasElement? canvas = querySelector('#circleCanvas') as CanvasElement?;
  
  // Check if the canvas was successfully selected
  if (canvas == null) {
    print('Canvas not found!');
    return;
  }

  // Get the 2D rendering context for the canvas
  CanvasRenderingContext2D ctx = canvas.getContext('2d') as CanvasRenderingContext2D;

  // Define the circle's diameter in centimeters and convert it to pixels
  double diameterCm = 5.0;                      // Diameter in cm
  double diameterPx = cmToPx(diameterCm);       // Convert diameter to pixels

  // Calculate the center coordinates and the radius of the circle
  double centerX = canvas.width! / 2;           // X-coordinate of the circle center
  double centerY = canvas.height! / 2;          // Y-coordinate of the circle center
  double radius = diameterPx / 2;                // Calculate the radius in pixels

  // Set the fill style for the circle (color)
  ctx.fillStyle = 'blue';  // Fill color for the circle
  
  // Begin drawing the circle
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, 2 * 3.141592653589793); // Full circle
  ctx.closePath();
  ctx.fill();  // Fill the circle
}


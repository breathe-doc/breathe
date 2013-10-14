/**
* The InteractionBox class represents a box-shaped region completely
* within the field of view of the Leap Motion controller.
*
* The interaction box is an axis-aligned rectangular prism and provides normalized
* coordinates for hands, fingers, and tools within this box. The InteractionBox class
* can make it easier to map positions in the Leap Motion coordinate system to 2D or
* 3D coordinate systems used for application drawing.
*
* \image html imageExample.png
*
* The InteractionBox region is defined by a center and dimensions along the x, y,
* and z axes.
*
* Get an InteractionBox object from a Frame object.
* @since 1.0
*/
class InteractionBox : public Interface {}



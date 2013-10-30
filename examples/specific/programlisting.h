
/*! Vector class */
class Vector {};

/*!
 * The center of the InteractionBox in device coordinates (millimeters). This point
 * is equidistant from all sides of the box.
 *
 * \include programlistinginclude.txt
 *
 * @returns The InteractionBox center in device coordinates.
 * @since 1.0
 */
LEAP_EXPORT Vector center() const;


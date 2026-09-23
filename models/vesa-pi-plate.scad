// VESA 100 plate carrying a Raspberry Pi (in a metal case) on the printhub display arm.
// Flat plate: VESA 100 holes at the corners, the Pi's 58 x 49 pattern at the centre,
// scalloped edges, hex-vented centre. Units mm; plate centred on the origin, Z0 = arm side.
//
//   openscad -o vesa-pi-plate.stl models/vesa-pi-plate.scad        (3D)
//   openscad -D mode=\"2d\" -o plan.svg models/vesa-pi-plate.scad  (plan-view outline)

mode = "3d";

plate   = 116;   // square envelope
corner  = 10;    // corner radius
thick   = 5;

vesa    = 100;   vesa_d = 4.5;    // M4 clearance
pi_x    = 58;    pi_y = 49;       // Raspberry Pi mounting pattern
pi_d    = 2.7;                    // M2.5 clearance
cb_d    = 6;     cb_h = 2;        // counterbore for M2.5 heads, arm side (Z0)
boss_r  = 6;     // solid ring kept around each Pi hole

scal_r  = 80;    // scallop arc radius
scal_d  = 14;    // scallop depth at edge midpoint

hex_w   = 6;     // hex hole across flats
hex_wall= 1.2;
vent_x  = 36;    vent_y = 33;     // vent field half-extents

$fn = 64;

module envelope() offset(r = corner) square(plate - 2 * corner, center = true);

module outline() difference() {
    envelope();
    for (a = [0, 90, 180, 270]) rotate(a)
        translate([0, plate / 2 + scal_r - scal_d]) circle(r = scal_r, $fn = 256);
}

module pi_holes() for (sx = [-1, 1], sy = [-1, 1]) translate([sx * pi_x / 2, sy * pi_y / 2]) children();
module vesa_holes() for (sx = [-1, 1], sy = [-1, 1]) translate([sx * vesa / 2, sy * vesa / 2]) children();

// Whole hexes only: a cell is cut when it lies entirely inside the vent field and clear of
// every Pi boss, so the field edge is a clean solid web rather than clipped slivers.
module vents() {
    p  = hex_w + hex_wall;              // pitch across flats
    rh = hex_w / 2 / cos(30);           // circumradius
    for (i = [-8 : 8], j = [-8 : 8]) {
        c = [i * p + (abs(j) % 2 - 0.5) * p / 2, j * p * sqrt(3) / 2];
        if (abs(c.x) + rh <= vent_x && abs(c.y) + rh <= vent_y
            && min([for (sx = [-1, 1], sy = [-1, 1]) norm(c - [sx * pi_x / 2, sy * pi_y / 2])])
               >= boss_r + rh)
            translate(c) rotate(30) circle(r = rh, $fn = 6);
    }
}

module profile() difference() {
    outline();
    vents();
    vesa_holes() circle(d = vesa_d);
    pi_holes() circle(d = pi_d);
}

if (mode == "2d") profile();
else difference() {
    linear_extrude(thick) profile();
    pi_holes() translate([0, 0, -0.01]) cylinder(d = cb_d, h = cb_h + 0.01);
}

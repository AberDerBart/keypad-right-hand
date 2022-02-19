include <KeyV2/includes.scad>
include <key_positions.scad>

include <labeledKeys.scad>

nKeys = 37;

$key_shape_type = "sculpted_square";
$bottom_key_width = 18.24; // 18.4;
$bottom_key_height = 18.24; // 18.4;
$width_difference = 6; // 5.7;
$height_difference = 6; // 5.7;
$top_skew = 0;
$dish_type = "cylindrical";
$dish_depth = 1.2;
$dish_skew_x = 0;
$dish_skew_y = 0;
$height_slices = 10;
$enable_side_sculpting = true;
$corner_radius = 1;

dsa_row(2)
let(
  $top_tilt=0,
  $dish_type = "cylindrical",
  $dish_depth = 1,
  $stem_type = "cherry",
  $stem_support_height = .4,
  $stem_inset = 0,
  $stem_slop = .1,
  $stem_inner_slop = $stem_slop,
  $cherry_bevel = true,
  //$support_type = "disable",
  $width_difference = 5,
  $height_difference = 5,
  $inset_legend_depth = 0.6,
  $cherry_bevel=true,
  $total_depth=6,
  $font="DejaVu Sans Mono:style=Book",
  $support_type="flat"
)
  
for(i = [0:nKeys]) {
  if (i != 7 && i != 11 && i != 16 && i != 17 && i != 18 && i != 20 && i != 27 && i < 32)
    positionedKey(i)labeledKey(i){
      key();
      key_brim();
    }
}


module key_brim() {
  unit = 19.05;
  linear_extrude(.2)
  difference(){
    square([$key_length * unit, $key_height * unit], center=true);
    square([$key_length * unit - 1, $key_height * unit - 1], center=true);

  }
}


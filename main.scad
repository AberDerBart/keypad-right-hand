include <KeyV2/includes.scad>
include <key_positions.scad>

include <labeledKeys.scad>

nKeys = len($key_positions) - 1;

*let(
  $dish_depth = 1,
  $stem_type = "cherry",
  $stem_support_height = .4,
  $stem_inset = 0,
  $stem_slop = .1,
  $stem_inner_slop = $stem_slop,
  $support_type = "disable",
  $corner_radius = 2,
  $width_difference = 4,
  $total_depth = $total_depth - 4,
  $inset_legend_depth = 0.4,
  $cherry_bevel = true,
  $rounded_cherry_stem_d = 6
){
  stem($stem_type, 6, 0, 0); 
  stem_support($stem_support_type,$stem_type, $stem_support_height, $stem_slop);
}


module custom_row(row) {
  let(
    $top_tilt = -max((row-3), 0)*7 -5,
    $total_depth = max((row-3), 0)*2+7
  ) children();
  
}

for(i = [0:nKeys]) {
  if($key_positions[i] != undef){
    x = $key_positions[i][0];
    y = $key_positions[i][1];
    w = $key_positions[i][2];
    h = $key_positions[i][3];

    //if(x==2 || x == 3)
    translate_u(x,y)
    u(w)
    uh(h)
    labeledKey(i)
    oem_row(0)
    let(
      $key_shape_type = "square",
      $dish_depth = 1,
      $stem_type = "cherry",
      $stem_support_height = .4,
      $stem_inset = 0,
      $stem_slop = .1,
      $stem_inner_slop = $stem_slop,
      $cherry_bevel = true,
      //$support_type = "disable",
      $width_difference = 4,
      $inset_legend_depth = 0.4,
      $font="DejaVu Sans Mono:style=Book"
    )custom_row(y){
      key();
      key_brim();
    }
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


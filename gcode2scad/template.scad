 
layer_height = .2;
 
layer_width = .4;
 
 module hull_polyline3d(points) {
    leng = len(points);
     
     module extr_unit() {  
         
            rotate_extrude(convexity = 2, $fn = 100)
            translate([layer_width/4, 0, 0])
            circle(d = layer_height, $fn = 100);
            
        }
         
    module hull_line3d(index) {
        point1 = points[index - 1];
        point2 = points[index];

        hull() {
            translate(point1) 
                extr_unit();               
            translate(point2) 
                extr_unit();               
        }       
               
        // hook for testing
        test_hull_polyline3d_line_segment(index, point1, point2);        
    }
    
    module polyline3d_inner(index) {
        if(index < leng) {
            hull_line3d(index);
            polyline3d_inner(index + 1);
        }
    }
    polyline3d_inner(1);
}

// override it to test
module test_hull_polyline3d_line_segment(index, point1, point2) {

}

echo("This is an Extrusion Unit with LAYER_HEIGHT=", layer_height, " and LAYER_WIDTH=", layer_width);

echo(layer_height=layer_height,layer_width=layer_width); // shortcut


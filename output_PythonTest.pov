// -w320 -h240

#version 3.6;

#include "colors.inc"
#include "textures.inc"
#include "shapes.inc"

global_settings {max_trace_level 5 assumed_gamma 1.0}

camera {
	location <-2.880000, 5.760000, -8.640000>
	direction <0, 0,  2.25>
	right x*1.33
	look_at <0,0,0>
}

#declare Dist=80.0;
light_source {< -25, 50, -50> color White
	fade_distance Dist fade_power 2
}
light_source {< 50, 10,  -4> color Gray30
	fade_distance Dist fade_power 2
}
light_source {< 0, 100,  0> color Gray30
	fade_distance Dist fade_power 2
}

sky_sphere {
	pigment {
		gradient y
		color_map {
			[0, 1  color White color White]
		}
	}
}

#declare Xaxis = union{
	cylinder{
		<0,0,0>,<0.8,0,0>,0.05
	}
	cone{
		<0.8,0,0>, 0.1, <1,0,0>, 0
	}
	texture { pigment { color Red } }
}
#declare Yaxis = union{
	cylinder{
		<0,0,0>,<0,0.8,0>,0.05
	}
	cone{
		<0,0.8,0>, 0.1, <0,1,0>, 0
	}
	texture { pigment { color Green } }
}
#declare Zaxis = union{
	cylinder{
	<0,0,0>,<0,0,0.8>,0.05
	}
	cone{
		<0,0,0.8>, 0.1, <0,0,1>, 0
	}
	texture { pigment { color Blue } }
}
#declare Axes = union{
	object { Xaxis }
	object { Yaxis }
	object { Zaxis }
}
#declare Material_SiO2 = texture{ pigment{ rgb <0.193304,0.563585,0.001251> } }
#declare Material_Si = texture{ pigment{ rgb <0.479873,0.585009,0.808741> } }
#declare Material_Vacuum = texture{ pigment{ color transmit 1.0 } }
#declare Layer_AirAbove = union{
/*
	difference{
		intersection{
			plane{ <0.960000,0.000000,0>, 0.480000 }
			plane{ <-0.960000,-0.000000,0>, 0.480000 }
			plane{ <0.000000,0.960000,0>, 0.480000 }
			plane{ <-0.000000,-0.960000,0>, 0.480000 }
			plane{ <0.960000,0.960000,0>, 0.678823 }
			plane{ <-0.960000,-0.960000,0>, 0.678823 }
			plane{ <0,0,-1>, 0 }
			plane{ <0,0,1>, 0.000000 }
		}
// nshapes = 0
		texture { Material_Vacuum }
	}
*/
	translate +z*0.000000
}
#declare Layer_AirDisp = union{
/*
	difference{
		intersection{
			plane{ <0.960000,0.000000,0>, 0.480000 }
			plane{ <-0.960000,-0.000000,0>, 0.480000 }
			plane{ <0.000000,0.960000,0>, 0.480000 }
			plane{ <-0.000000,-0.960000,0>, 0.480000 }
			plane{ <0.960000,0.960000,0>, 0.678823 }
			plane{ <-0.960000,-0.960000,0>, 0.678823 }
			plane{ <0,0,-1>, 0 }
			plane{ <0,0,1>, 1.000000 }
		}
// nshapes = 0
		texture { Material_Vacuum }
	}
*/
	translate +z*0.000000
}
#declare Layer_Si_disks = union{
/*
	difference{
		intersection{
			plane{ <0.960000,0.000000,0>, 0.480000 }
			plane{ <-0.960000,-0.000000,0>, 0.480000 }
			plane{ <0.000000,0.960000,0>, 0.480000 }
			plane{ <-0.000000,-0.960000,0>, 0.480000 }
			plane{ <0.960000,0.960000,0>, 0.678823 }
			plane{ <-0.960000,-0.960000,0>, 0.678823 }
			plane{ <0,0,-1>, 0 }
			plane{ <0,0,1>, 0.220000 }
		}
// nshapes = 1
cylinder{
	<0,0,0>, <0,0,0.220000>, 0.365000
	rotate +z*0.000000
	translate +x*0.000000
	translate +y*0.000000
}
		texture { Material_Vacuum }
	}
*/
	difference{
		intersection{
cylinder{
	<0,0,0>, <0,0,0.220000>, 0.365000
	rotate +z*0.000000
	translate +x*0.000000
	translate +y*0.000000
}
			plane{ <0,0,-1>, 0 }
			plane{ <0,0,1>, 0.220000 }
		}
		texture { Material_Si }
	}
	translate +z*1.000000
}
#declare Layer_Glass_Below = union{
	difference{
		intersection{
			plane{ <0.960000,0.000000,0>, 0.480000 }
			plane{ <-0.960000,-0.000000,0>, 0.480000 }
			plane{ <0.000000,0.960000,0>, 0.480000 }
			plane{ <-0.000000,-0.960000,0>, 0.480000 }
			plane{ <0.960000,0.960000,0>, 0.678823 }
			plane{ <-0.960000,-0.960000,0>, 0.678823 }
			plane{ <0,0,-1>, 0 }
			plane{ <0,0,1>, 2.000000 }
		}
// nshapes = 0
		texture { Material_SiO2 }
	}
	translate +z*1.220000
}
#declare Layer_AirBelow = union{
/*
	difference{
		intersection{
			plane{ <0.960000,0.000000,0>, 0.480000 }
			plane{ <-0.960000,-0.000000,0>, 0.480000 }
			plane{ <0.000000,0.960000,0>, 0.480000 }
			plane{ <-0.000000,-0.960000,0>, 0.480000 }
			plane{ <0.960000,0.960000,0>, 0.678823 }
			plane{ <-0.960000,-0.960000,0>, 0.678823 }
			plane{ <0,0,-1>, 0 }
			plane{ <0,0,1>, 0.000000 }
		}
// nshapes = 0
		texture { Material_Vacuum }
	}
*/
	translate +z*3.220000
}
#declare Layers = union {
	//object{ Layer_AirAbove }
	object{ Layer_AirDisp }
	object{ Layer_Si_disks }
	object{ Layer_Glass_Below }
	//object{ Layer_AirBelow }
}

Axes
Layers

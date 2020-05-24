---VERTEX SHADER-------------------------------------------------------
/**
* Based on: https://learnopengl.com/Advanced-Lighting/Advanced-Lighting
*/

#ifdef GL_ES
    precision highp float;
#endif

attribute vec3  v_pos;
attribute vec3  v_normal;
attribute vec4  v_color;
attribute vec2  v_tc0;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;

varying vec4 frag_color;
varying vec2 uv_vec;
varying vec4 normal_vec;
varying vec4 vertex_pos;

void main (void) {
    vec4 pos = modelview_mat * vec4(v_pos,1.0);
    vertex_pos = pos;
    gl_Position = projection_mat * pos;
    frag_color = v_color;
    uv_vec = v_tc0;
    normal_vec = modelview_mat * vec4(v_normal, 0.0);
}


---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 frag_color;
varying vec2 uv_vec;
varying vec4 normal_vec;
varying vec4 vertex_pos;

uniform mat4 normal_mat;
uniform sampler2D tex;

uniform vec3 light_pos;
uniform float light_intensity;
uniform vec3 camera_pos;

uniform vec3 Ka; // color (ambient)
uniform vec3 Kd; // diffuse color
uniform vec3 Ks; // specular color
uniform float Tr; // transparency
uniform float Ns; // shininess
uniform float d; // dissolve
uniform float ambient_ratio;

void main (void){
    vec4 color = texture2D(tex, uv_vec);
    color = vec4(Ka, Tr);
    if (Ns > 0.0) {
        // ambient
        vec3 ambient = ambient_ratio * vec3(color);
        // diffuse
        vec3 lightDir = normalize(light_pos - vec3(vertex_pos));
        vec3 normal = normalize(vec3(normal_vec));
        float diff = max(dot(lightDir, normal), 0.0);
        vec3 diffuse = diff * vec3(Kd);
        // specular
        vec3 viewDir = normalize(camera_pos - vec3(vertex_pos));
        vec3 reflectDir = reflect(-lightDir, normal);

        // Blinn-Phong lighting
        vec3 halfwayDir = normalize(lightDir + viewDir);
        float spec = pow(max(dot(normal, halfwayDir), 0.0), Ns);

//        vec3 specular = vec3(0.3) * spec;// assuming bright white light color
        vec3 specular = Ks * spec;// assuming bright white light color
        gl_FragColor = vec4(ambient + diffuse + specular, color[3]);
    } else {
        gl_FragColor = color;
    }
}

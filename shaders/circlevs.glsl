#version 330

layout(location = 0) in vec2 position;

uniform mat4 camToClipMat;
uniform mat4 modelToCamMat;

void main()
{
    gl_Position = camToClipMat * (modelToCamMat * vec4(position, 0, 1));
    // gl_Position = vec4(position, 1);
}

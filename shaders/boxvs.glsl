#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec4 color;

uniform mat4 camToClipMat;
uniform mat4 modelToCamMat;

smooth out vec4 theColor;

void main()
{
    gl_Position = camToClipMat * (modelToCamMat * vec4(position, 1));
    // gl_Position = vec4(position, 1);
    theColor = color;
}

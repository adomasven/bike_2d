#version 330

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;

smooth out vec4 theColor;

uniform mat4 modelToWorldMat;
uniform mat4 worldToCamMat;

void main()
{
    gl_Position = worldToCamMat * (modelToWorldMat * position);
    theColor = color;
}

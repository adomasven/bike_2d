#version 330

layout(location = 0) in vec2 position;
layout(location = 1) in vec2 vertTexCoord;

uniform mat4 transformMat;

out vec2 fragTexCoord;

void main()
{
    gl_Position = transformMat * vec4(position, 0, 1);
    // gl_Position = vec4(position, 0, 1);
    fragTexCoord = vertTexCoord;
}

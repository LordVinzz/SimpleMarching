from math import *
from pygame import *
import asyncio

PI = 3.1415926535

class Ray:

    def __init__(self,x,y,z,longitude,latitude):
        self.x = x
        self.y = y 
        self.z = z 

        self.SIN_LATITUDE = sin(latitude)
        self.SIN_LONGITUDE = sin(longitude)

        self.COS_LATITUDE = cos(latitude)
        self.COS_LONGITUDE = cos(longitude)

        self.nbrSteps = 0
        self.collision = False
        self.sphereInstance = None


    def setInformations(self, nbrSteps, collision, sphereInstance):
        self.nbrSteps = nbrSteps
        self.collision = collision
        self.sphereInstance = sphereInstance

    def stepRay(self,step):
        self.x += self.COS_LONGITUDE * self.COS_LATITUDE * step
        self.y += self.COS_LATITUDE * self.SIN_LONGITUDE * step
        self.z += self.SIN_LATITUDE * step

class Material:
    
    def __init__(self,albedo,emission,color):
        self.albedo = albedo
        self.emission = emission
        self.color = color

class Sphere:

    def __init__(self,x,y,z,r,material):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.material = material
    
    def distanceTo(self,x,y,z):
        return sqrt( (x-self.x)**2 + (y-self.y)**2 + (z-self.z)**2 ) - self.r
    
    def getNormal(self,x,y,z):
        return Vector3(x-self.x,y-self.y,z-self.z).normalize()
    
    def getMaterial(self):
        return self.material
    
    def getAlbedo(self):
        return self.material.albedo
    
    def getEmission(self):
        return self.material.emission
    
    def getColor(self):
        return self.material.color
    
    
class Camera:
    
    def __init__(self,x,y,z,width,height,phi,theta):
        self.maxSize = 0.001
        self.x = x
        self.y = y
        self.z = z
        self.phi = phi
        self.theta = theta
        self.width = width
        self.height = height
        
    #TODO shoot ray from full position and not just screen space 
    def shootRay(self,scene,pixelX,pixelY):

        ratio = self.width / self.height

        longitude = pixelX * PI / self.width + self.phi
        latitude = pixelY * PI / (self.height * ratio) + self.theta

        ray = Ray(self.x,self.y,self.z,longitude,latitude)
        nbrSteps = 0
        (stepSize, sphereInstance) = scene.getDistToScene(ray.x,ray.y,ray.z)
        collision = stepSize < self.maxSize

        while nbrSteps <= 10 and not collision:
            ray.stepRay(stepSize)
            (stepSize, sphereInstance) = scene.getDistToScene(ray.x,ray.y,ray.z)
            nbrSteps +=1
            collision = stepSize < self.maxSize

        ray.setInformations(nbrSteps,collision,sphereInstance)
        return ray
       
            

class Scene:

    def __init__(self, width, height):
        self.spheres = [Sphere(15,-45,0,25, Material(0.5,0.5,(0,255,0))),
                        Sphere(15,45,-0,25, Material(0.5,0.5,(0,0,255)))]

        self.camera = Camera(0,0,0,width,height,0,0)
        self.width = width
        self.height = height

        assert width > 0 and height > 0 and width % 2 == 0 and height % 2 == 0, "Width and height must be even and positive"

        init()
        self.window = display.set_mode((width,height))
        self.window.fill((0,0,0))

    def getDistToScene(self,x,y,z):
        minDist = self.spheres[0].distanceTo(x,y,z)
        sphereInst = self.spheres[0]

        for i in range(1,len(self.spheres)):

            calc = self.spheres[i].distanceTo(x,y,z)

            if minDist > calc:
                sphereInst = self.spheres[i]
                minDist = calc
            
        return (minDist, sphereInst)

    def render(self):
        
        halfWidth = self.width//2
        halfHeight = self.height//2

        

        for x in range(-halfWidth,halfWidth):
            for y in range(-halfHeight,halfHeight):
                ray = self.camera.shootRay(self,x,y)
                if ray.collision:
                    vector = ray.sphereInstance.getNormal(ray.x,ray.y,ray.z)
                    vector2 = vector.cross(Vector3(ray.x, ray.y, ray.z))
                    ray2 = self.camera.shootRay(vector2.x,vector2.y,vector2.z)
                    self.window.set_at((x+halfWidth,y+halfHeight), ray2.sphereInstance.getColor())
            display.flip()

    def wait(self):
        running = True
        while running:
            for evt in event.get():
                if evt.type == QUIT:
                    running = False
        quit()

scene = Scene(300,300)
scene.render()
scene.wait()

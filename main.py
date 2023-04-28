from math import *
from pygame import *

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
        return (x-self.x,y-self.y,z-self.z)
    
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
        

    def shootRay(self,scene,pixelX,pixelY):

        longitude = pixelX * PI / self.width + self.phi
        latitude = pixelY * PI / self.height + self.theta

        rayon = Ray(self.x,self.y,self.z,longitude,latitude)
        nbPas = 0
        (stepSize, sphereInstance) = scene.getDistToScene(rayon.x,rayon.y,rayon.z)
        collision = stepSize < self.maxSize

        while nbPas <= 10 and not collision:
            rayon.stepRay(stepSize)
            (stepSize, sphereInstance) = scene.getDistToScene(rayon.x,rayon.y,rayon.z)
            nbPas +=1
            collision = stepSize < self.maxSize
        return (collision,nbPas,sphereInstance)
    
            

class Scene:

    def __init__(self):
        self.spheres = [Sphere(15,5,-3,10, Material(0.5,0.5,(255,0,0))),
                        Sphere(15,-5,-3,10, Material(0.5,0.5,(0,255,0))),
                        Sphere(15,0,3,10, Material(0.5,0.5,(0,0,255))),]

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
        bismillahCam = Camera(0,0,0,200,200,0,0)
        for x in range(-100,100):
            for y in range(-100,100):
                (collision,nbPas,sphereInstance) = bismillahCam.shootRay(self,x,y)
                if collision:
                    window.set_at((x+100,y+100),sphereInstance.getColor())


init()
window = display.set_mode((200,200))

window.fill((0,0,0))
scene = Scene()
scene.render()

display.flip()
running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
quit()
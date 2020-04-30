from fpdf import FPDF
pdf = FPDF()


goal = int(input("What is your learning goal? "))
print("you chose learning goal " + str(goal))

imagelist = ["octopus.png", "owl.png", "cat.png", "dog.png"]

pdf.add_page()
pdf.image(imagelist[goal],10,10) #you can add two more parameters here for width and height, but they mess up the aspect ratio
pdf.output("yourfile.pdf", "F")
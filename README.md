# Pynamation
Tkinter based animation library for python. This readme is currently incomplete.

## Functions:
In this section, required arguments are shown in angled brackets, while optional arguments are shown in curly brackets.

#### General Utilities:
* **title:** Set the window title. `title("<Window Title>")`
* **createCanvas:** Set the window size. `createCanvas(<Width>, <Height>)`
* **canvasFunction:** Retrieve the canvas. Useful for calling canvas-related tasks outside of this module. `canvasFunction()`
* **setFrameRate:** Set the rate at which the canvas is updated. This is set automatically to 63. `setFrameRate(<Integer>)`
* **displayFrameRate:** Display the frame rate as text. `displayFrameRate(<Current Time>, <X>, <Y>, color="{Color}", anchor="{Anchor}")`
 
**Some things to keep in mind:**
You need a function that contains `canvasFunction().after(framerateDelay,functionNameHere)` for the frames to update. The file must end with `mainloop()`.

#### Drawing Objects:
* **rect:** Draw a rectangle. `rect(<X>, <Y>, <Width>, <Height>, fill="{Fill}", tag="{Tag}")`
* **ellipse:** Draw an ellipse. `ellipse(<X>, <Y>, <Width>, <Height>, fill="{Fill}", tag="{Tag}")`
* **text:** Draw text. `text(<X>,<Y>,text="{Text}",fill="{Fill}",fontFace="{Font}", fontSize={Integer}, fontStyle="{Font Style}", anchor="{Anchor}",tag="{Tag}")`
* **polygon:** Will be implemented in the future.
* **changeFill:** Change the color of an object. `changeFill("<Tag>", "<Fill>")` or `changeFill(<Object>, "<Fill>")`
* **changeText:** Change the text of a text object. `changeText("<Tag>", "<New Text>")` or `changeText(<Object>, "<New Text>")`
* **deleteShape:** Delete an object. `deleteShape("<Tag>")` or `deleteShape(<Object>)`

#### Working with Images:
###### Static Images:
Create an image variable using `<Image> = PhotoImage(file="<File Name>")`.
To zoom in, use `<Image> = <Image>.zoom(<Integer>)`.
###### Animated Images:
Create an image to animate using `<Image> = ImgAnimation(<Image>, <Amount>, <X>, <Y>, zoom={Integer}, anchor="{Anchor}", delay={Integer})`.
To animate the image call `<Image>.animate(<X>, <Y>, isTrigger={Boolean})`.

#### Miscellaneous:
* **playSound:** Play a sound (This will only work on Windows systems). `playSound("<Sound File>")`
* **setCursor:** Change the mouse cursor. `setCursor("<Cursor>")`
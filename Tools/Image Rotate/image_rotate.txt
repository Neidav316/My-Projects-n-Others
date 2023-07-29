

let angle = 0; // Default value
let selectedImage = null; // no selected canvas/image to rotate on default
const imageList = document.querySelector(".output-div");
const imageSelector = document.querySelector("#in-img");
const CANVAS_MARGIN = 60;
const CANVAS_SIZE = 200;


imageSelector.addEventListener("input",function() {addImages(imageSelector.files)});

function changeAngleInput(){
  let value = document.getElementById("angle-field").value;
  if (isNaN(value))
    document.getElementById("error-angle").innerHTML = "Error, only number values";
  else 
    document.getElementById("error-angle").innerHTML = "";

}

function changeImageAngle(direction){
  let value = document.getElementById("angle-field").value;
  if (value == "" || isNaN(value))
    alert("Please enter the angle amount you wish to change");
  else if (selectedImage == null)
    alert("Please select an image to rotate");
  else {
    angle = value * direction;
    rotate();
  }
}


function addImages(files){

  for (const file of files){
    const canvas = document.createElement("canvas");
    const img = new Image();
    canvas.height = CANVAS_SIZE;
    canvas.width = CANVAS_SIZE;
    canvas.classList.add("canvas");
    const contx = canvas.getContext("2d");
    img.onload = () => {contx.drawImage(img,0,0,img.width,img.height,CANVAS_MARGIN/2,CANVAS_MARGIN/2,canvas.width-CANVAS_MARGIN,canvas.height-CANVAS_MARGIN); };
    canvas.onclick = () => { 
      if(selectedImage != null)
        selectedImage.style.border = "0px solid white"
      selectedImage = canvas;
      selectedImage.style.border = "3px solid yellow";};
    canvas.style.left = randomInt(0,imageList.offsetWidth-CANVAS_SIZE)+"px"; // - 200px of the canvas
    canvas.style.top = randomInt(0,imageList.offsetHeight-CANVAS_SIZE)+"px";
    img.src = URL.createObjectURL(file);
    
    imageList.appendChild(canvas);

    const reader = new FileReader();
    reader.onload = (e) => {img.src = e.target.result;};
    reader.readAsDataURL(file);
    document.getElementById("no-img-msg").innerHTML = "";

  }
  imageSelector.value = null;
  
}

function rotate(){
  let src = cv.imread(selectedImage);
  let dst = new cv.Mat(src);
  let dsize = new cv.Size(src.rows, src.cols);
  let center = new cv.Point(src.cols / 2, src.rows / 2);

  let M = cv.getRotationMatrix2D(center, angle, 1);
  cv.warpAffine(src, dst, M, dsize, cv.INTER_LINEAR, cv.BORDER_CONSTANT, new cv.Scalar());
  cv.imshow(selectedImage, dst);
  src.delete(); dst.delete(); M.delete();
}

function randomInt(min, max) {
  return Math.floor(Math.random() *(max-min)) + min;
}

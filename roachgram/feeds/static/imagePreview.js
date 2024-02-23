
                

const preview = (e) => {
    // const [file] = imgInp.files
    // if (file) {
    //     blah.src = URL.createObjectURL(file)
    // }
    const files =  Array.from(e.files)
    files.forEach(file => {
      const blob = URL.createObjectURL(file)
      if (file.type.includes("image")){ 
        
        
        document.querySelector(".parent-for-preview").innerHTML += `
                <div class="flex m-1 flex-wrap cursor-pointer">
                    <div class="w-full">
                        <img
                            alt="gallery"
                            class="block h-44 w-44 rounded-lg object-cover object-center"
                            src="${blob}" />
                    </div>             
                </div>

        `
      }
      else if(file.type.includes("video")){
        document.querySelector(".parent-for-preview").innerHTML += `
                <div class="flex m-1 flex-wrap cursor-pointer">
                    <div class="w-full">
                        <video
                            controls
                            alt="gallery"
                            class="block h-44 w-44 rounded-lg object-cover object-center"
                            src="${blob}">
                        </video>
                    </div>             
                </div>
        `
      }
    })
}
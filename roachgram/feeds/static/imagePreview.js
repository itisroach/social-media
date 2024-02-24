const preview = (e) => {
    const files = Array.from(e.files)
  
    files.forEach(file => {

      const blob = URL.createObjectURL(file)
      if (file.type.includes("image")){         
        document.querySelector(".parent-for-preview").innerHTML += `
                      <div class="flex relative w-auto h-auto m-0.5 flex-wrap cursor-pointer">
                        <div class="w-full w-auto h-auto">
                          <img
                            alt="gallery"
                            class="h-full w-auto h-auto rounded-lg object-cover object-center"
                            src="${blob}" />
                        </div>             
                      </div>

        `
      }
      else if(file.type.includes("video")){
        document.querySelector(".parent-for-preview").innerHTML += `
                      <div class="flex relative w-auto h-auto m-0.5 flex-wrap cursor-pointer">
                      <div class="w-full w-auto h-auto">
                        <video
                          controls
                          alt="gallery"
                          class="h-full w-auto h-auto rounded-lg object-cover object-center"
                          src="${blob}">
                          </video>
                      </div>             
                    </div>
        `
      }
    })
}
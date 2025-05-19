class NavBar {
    constructor() {
      this.clicked = false
      this.menus = document.getElementsByClassName("nav-menu")
      this.sub_menus_title = document.getElementsByClassName("nav-sub-menu-title")
      this.sub_menus = document.getElementsByClassName("nav-sub-menu")
    }
  
    clicked_func() {
      if (this.clicked) {
        this.clicked = false
        for (let i = 0; i < this.sub_menus.length; i++) {
          /* this.sub_menus_title[i].removeEventListener("click", function () {} );*/
          if (!this.sub_menus[i].classList.contains("hidden")) {
            this.sub_menus[i].classList.add("hidden")
          }
        }
        for (let i = 0; i < this.menus.length; i++) {
          this.menus[i].classList.add("hidden")
        }
      } else {
        this.clicked = true
  
        for (let i = 0; i < this.menus.length; i++) {
          this.menus[i].classList.remove("hidden")
        }
        if (this.test_run) {
          return
        } else {
          test()
          this.test_run = true
        }
      }
    }
  
    sub_clicked_func(iterator, menus) {
      const target = menus[iterator]
      for (let i = 0; i < menus.length; i++) {
        if (iterator == i) {
          if (target.classList.contains("hidden")) {
            target.classList.remove("hidden")
          } else {
            target.classList.add("hidden")
          }
        } else {
          if (menus[i].classList.contains("hidden")) {
            continue
          } else {
            menus[i].classList.add("hidden")
          }
        }
      }
    }
  }
  
  if (window.screen.width) {
      const classes = document.getElementsByClassName("nav-menu");
      for(let i=0; i < classes.length; i++) {
          classes[i].classList.remove("hidden");
      }
  }
  
  let nav = new NavBar()
  
  document.getElementById("nav-bar-title").addEventListener("click", function () {
    nav.clicked_func(nav)
  })
  
  // Creating outside class function to add event listeners since I cannot use keyword 'this' to declare event listener with class properties INSIDE class method.
  function test() {
    for (let i = 0; i < nav.sub_menus_title.length; i++) {
      nav.sub_menus_title[i].addEventListener("click", function () {
        nav.sub_clicked_func(i, nav.sub_menus)
        console.log(`Clicked: ${nav.sub_menus_title[i].innerText}`)
      })
    }
  }
  
  
  
  // NEW FILE ************************************************************
  class HighlightImageSlideShow {
      constructor() {
          this.element = document.getElementById("highlight-picture");
          this.text = document.getElementById("highlight-picture-text");
          this.pictures = ["https://images.pexels.com/photos/139309/pexels-photo-139309.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", "https://images.pexels.com/photos/942305/pexels-photo-942305.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", "https://as2.ftcdn.net/v2/jpg/04/28/76/95/1000_F_428769564_NB2T4JM9E2xsxFdXXwqW717HwgaZdpAq.jpg"];
      }
      
      change_picture(obj) {
          for(let i = 0; i < obj.pictures.length; i++) {
              if (obj.element.src == obj.pictures[i]) {
                  if (i < obj.pictures.length-1) {
                      obj.element.src = `${obj.pictures[i+1]}`;
                      break;
                  } else {
                      obj.element.src = obj.pictures[0];
                      break
                  }
              } else if (obj.element.src == "undefined") {
                  obj.element.src = obj.pictures[0];
              }
          }
      }
  }
  
  const highlight_image = new HighlightImageSlideShow();
  setInterval(function() {highlight_image.change_picture(highlight_image)}, 5000)
  // END OF FILE ***********************************************************************
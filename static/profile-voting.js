container = document.querySelector(".main-container"),
pwShowHide = document.querySelectorAll(".showHidePw"),
pwFields = document.querySelectorAll(".password");

// js code to change password view

pwShowHide.forEach(eyeIcon =>{
    eyeIcon.addEventListener("click", () =>{
        pwFields.forEach(pwField =>{
            if(pwField.type ==="password"){
                pwField.type = "text";

                pwShowHide.forEach(icon =>{
                    icon.classList.replace("uil-eye-slash", "uil-eye");
                })
            }else{
                pwField.type = "password";

                pwShowHide.forEach(icon =>{
                    icon.classList.replace("uil-eye", "uil-eye-slash");
                })
            }
        })
    })
})

// $(document).ready(function(){
//     onPageLoad();

//     $("button").click(function(){
//         $(".allSection").hide();
//         var parent=$('section');
//         var element = $(this).parent().is(':last-child');
//         if($(this).parent().is(':last-child'))
//             $('.firstTimeLoad').show();
//         else
//         $(this).parent().next().show();
        
//     });
// });

// function onPageLoad(){
//     $(".allSection").hide();
//     $(".firstTimeLoad").show();
// }

// $(document).ready(function(){
//     $('.allSection:not(:first-child)').hide();
   
//     $(".allSection button").click(function(){
//         $('.allSection').hide();

//         if( $(this).closest('.allSection').is(':last-child') ){
//             $(this).closest('.allSection').siblings().first().show();
//         }else{
//             $(this).closest('.allSection').next().show();
//         }
//     });  
// });


(() => {
    "use strict";
    
    document.querySelectorAll("button").forEach((e) => {
        e.addEventListener("click", showNext);
    });
    
    function showNext(e) {
        let nextId, sectionId;
        sectionId = parseInt(e.target.getAttribute("data-section-id"));
        document.getElementById(`section-${sectionId}`).style.display = "none";
    
        // Next section id
        if (sectionId == 3) {
            nextId = 1;
        } else {
            // Get section id
            nextId = sectionId + 1;
        }
        document.getElementById(`section-${nextId}`).style.display = "block";
    }
    })();
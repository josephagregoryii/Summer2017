var likes = document.getElementById("likes")
var shares = document.getElementById("shares")
var comments = document.getElementById("comments")
var feeds = document.getElementById("feeds")
var post_img = document.getElementById("post_image")
var succeeded = document.getElementById("succeeded")

if (succeeded.textContent == "1") {
    succeeded.textContent = "Yes"
} else {
    succeeded.textContent = "No"
}

if (post_img.getAttribute("src") == "") {
    post_img.style.visibility = "hidden"
}
if (likes.textContent == " NA") {
    likes.style.color = "white"
}

if (shares.textContent == " NA") {
    shares.style.color = "white"
}

if (comments.textContent == " NA") {
    comments.style.color = "white"
}

var before_id_btn = document.getElementById("before_btn")
var after_id_btn = document.getElementById("after_btn")

if (before_id_btn.getAttribute("href") == "/0") {
    before_id_btn.style.visibility = "hidden"
}

if (after_id_btn.getAttribute("href") == "/0") {
    after_id_btn.style.visibility = "hidden"
}
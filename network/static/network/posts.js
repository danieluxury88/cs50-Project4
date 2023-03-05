document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.getElementById('profile_view_btn').addEventListener('click', () => show_current_view('profile_view'));
    document.getElementById('posts_view_btn').addEventListener('click', () => show_current_view('posts_view'));
    document.getElementById('following_posts_btn').addEventListener('click', () => show_current_view('posts_view', "following"));

    show_default_page();

    //TEST
    document.getElementById('test_btn').addEventListener('click', () => test_function());
});

function test_function() {
    console.log("Test button");
    fetch('/test')
        .then(test_response => test_response.json())
        .then(test_data => {
            console.log(test_data);
            console.log(test_data.author);
            console.log(test_data.content);
            console.log(test_data.timestamp);
        })
        .catch(error => console.error(error));

}


function highlight_selected_item(btn) {
    const profileButton = document.getElementById('profile_view_btn');
    profileButton.classList.remove("selected_item");

    const feedButton = document.getElementById('posts_view_btn');
    feedButton.classList.remove("selected_item");

    const following_posts = document.getElementById('following_posts_btn');
    following_posts.classList.remove("selected_item");

    const selected_item = document.getElementById(btn);
    selected_item.classList.add("selected_item")
}

function show_current_view(view, type = "all") {

    console.log(view, type);
    // Show compose view and hide other views
    document.getElementById('posts_view').style.display = 'none';
    document.getElementById('profile_view').style.display = 'none';
    const current_view = document.getElementById(view);
    current_view.style.display = 'block';
    current_view.innerHTML = '';

    if (view == 'profile_view') {
        show_profile(current_view)
    }
    else if (view == 'posts_view') {
        show_feed(current_view, type)

    }
}

function show_profile(current_view) {
    highlight_selected_item('profile_view_btn');
    current_view.innerHTML = `
        <h1>Profile</h1>
    `;

    fetch(`/profile`)
        .then(test_response => test_response.json())
        .then(test_data => {
            console.log(test_data);
        })
        .catch(error => console.error(error));

}

function show_default_page() {
    show_current_view('posts_view');
}

function show_feed(current_view, feed_type) {
    console.log(feed_type);
    fetch(`/feed/${feed_type}`)
        .then(test_response => test_response.json())
        .then(test_data => {
            console.log(test_data);
        })
        .catch(error => console.error(error));
}
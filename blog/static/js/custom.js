$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    }
});

$('.reply-button').click(e => {
  $(e.target).parents('.card-body').children('.reply-border').children('.reply-form').toggle()
});

$('.comment-btn').click(function(){
  $('#comment-form').toggle();
});

$(document).on('submit', '#comment-form', function(event){
  event.preventDefault();
  const slug = $('#slug').first().data('slug');
  console.log(event, $(event.target))
  const data = {
    content: $(event.target).find('.form-control').val()
   }

  $.ajax({
    method: 'POST',
    url: `/post/${slug}/`,
    data: data,
    dataType: 'json',
    success: function(response) {
      $('main-comment-section').html(response['form']);
      $('textarea').val('');
      $('#comment-form').toggle();
    },
    error: function(rs, e) {
      console.log(rs.responseText);
    },
  })
})

$(document).on('submit', '.reply-form', function(event){
  const slug = $('#slug').first().data('slug');

  event.preventDefault();
  console.log(event)
 const data = {
  comment_id: $(event.target).find('.reply-comment-id').val(),
  content: $(event.target).find('.form-control').val()
 }

  $.ajax({
    method: 'POST',
    url: `/post/${slug}/`,
    data: data,
    dataType: 'json',
    success: function(response) {
      $(event.target).parents('.reply-form').hide()
      $('main-comment-section').html(response['form']);
      $('textarea').val('');
    },
    error: function(rs, e) {
      console.log(rs.responseText);
    },
  })
  event.preventDefault();
})

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function getCSRFToken()
{
  return getCookie('csrftoken');
}

});
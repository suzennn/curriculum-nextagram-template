// Handle follow & unfollow btn
$(document).ready(function() {
    $('.follow-click').on('click', function(e) {
        e.preventDefault()
        if($('.follow-click').text() == "follow" && e.target.title != "private"){
            $.ajax({
                url: `/users/follow/${e.target.id}`,
                method: 'GET',
                beforeSend: function() {
                $('.follow-click')
                    .prop('disabled', true)
                    .text('Loading...')
                },
                success: function(response) {
                $('#followers-count').text(response.new_follower_count)
                $('.follow-click')
                    .prop('disabled', false)
                    .removeClass('btn-follow')
                    .addClass('btn-outline-follow')
                    .text('unfollow')
                }
            })
        } else if ($('.follow-click').text() == "follow" && e.target.title == "private"){
            $.ajax({
                url: `/users/follow/${e.target.id}`,
                method: 'GET',
                beforeSend: function() {
                $('.follow-click')
                    .prop('disabled', true)
                    .text('Loading...')
                },
                success: function(response) {
                $('#followers-count').text(response.new_follower_count)
                $('.follow-click')
                    .prop('disabled', false)
                    .removeClass('btn-follow')
                    .addClass('btn-danger')
                    .text('pending')
                }
            })          
        } else{
            $.ajax({
                url: `/users/unfollow/${e.target.id}`,
                method: 'GET',
                beforeSend: function() {
                $('.follow-click')
                    .prop('disabled', true)
                    .text('Loading...')
                },
                success: function(response) {
                $('#followers-count').text(response.new_follower_count)
                $('.follow-click')
                    .prop('disabled', false)
                    .removeClass('btn-outline-follow')
                    .removeClass('btn-danger')
                    .addClass('btn-follow')
                    .text('follow')
                }
            })
        }
    })
})

// accept follow request
$(document).ready(function() {
    $('.accept').on('click', function(e) {
        id_name = e.target.id.toString()
        id_num = id_name.substring(7,id_name.length)
        e.preventDefault()
        $.ajax({
            url: `/users/accept-request/${id_num}`,
            method: 'GET',
            beforeSend: function() {
            $(`#${e.target.id}`)
                .prop('disabled', true)
                .text('Loading...')
            },
            success: function(response) {
            $('#followers-count').text(response.new_follower_count)
            $(`#${e.target.id}`)
                .prop('disabled', false)
                .text('Accepted')
                .removeClass('btn-info')
                .addClass('btn-dark')
            }
        })
    })
})

// reject follow request
$(document).ready(function() {
    $('.reject').on('click', function(e) {
        id_name = e.target.id.toString()
        id_num = id_name.substring(7,id_name.length)
        e.preventDefault()
        $.ajax({
            url: `/users/reject-request/${id_num}`,
            method: 'GET',
            beforeSend: function() {
            $(`#${e.target.id}`)
                .prop('disabled', true)
                .text('Loading...')
            },
            success: function(response) {
            $('#followers-count').text(response.new_follower_count)
            $(`#${e.target.id}`)
                .prop('disabled', false)
                .text('Rejected')
                .removeClass('btn-danger')
                .addClass('btn-dark')
            }
        })
    })
})

//follow in homepage
$(document).ready(function() {
    $('.follow-link').on('click', function(e) {
        console.log(e)
        e.preventDefault()
        id_name = e.target.id.toString()
        id_num = id_name.substring(7,id_name.length)
        if($(`#${e.target.id}`).text() == "follow" && e.target.title != "private"){
            $.ajax({
                url: `/users/follow/${id_num}`,
                method: 'GET',
                beforeSend: function() {
                $(`#${e.target.id}`)
                    .prop('disabled', true)
                    .text('loading...')
                },
                success: function(response) {
                $('#followers-count').text(response.new_follower_count)
                $(`#${e.target.id}`)
                    .prop('disabled', false)
                    .removeClass('text-primary')
                    .addClass('text-dark')
                    .text('unfollow')
                }
            })
        } else if ($(`#${e.target.id}`).text() == "follow" && e.target.title == "private"){
            $.ajax({
                url: `/users/follow/${id_num}`,
                method: 'GET',
                beforeSend: function() {
                $(`#${e.target.id}`)
                    .prop('disabled', true)
                    .text('loading...')
                },
                success: function(response) {
                $('#followers-count').text(response.new_follower_count)
                $(`#${e.target.id}`)
                    .prop('disabled', false)
                    .removeClass('text-primary')
                    .addClass('text-danger')
                    .text('pending')
                }
            })          
        } else{
            $.ajax({
                url: `/users/unfollow/${id_num}`,
                method: 'GET',
                beforeSend: function() {
                $(`#${e.target.id}`)
                    .prop('disabled', true)
                    .text('Loading...')
                },
                success: function(response) {
                $('#followers-count').text(response.new_follower_count)
                $(`#${e.target.id}`)
                    .prop('disabled', false)
                    .removeClass('text-dark')
                    .removeClass('text-danger')
                    .addClass('text-primary')
                    .text('follow')
                }
            })
        }
    })
})
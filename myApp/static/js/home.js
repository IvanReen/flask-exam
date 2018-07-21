$(function() {
	var swiper = new Swiper('.swiper-container', {
		pagination: '.swiper-pagination',
		paginationClickable: true,
		nextButton: '.swiper-button-next',
		prevButton: '.swiper-button-prev',
		spaceBetween: 30,
		effect: 'fade'
	});


	$.getJSON('/api/v1/banner/', function (response) {
        arr = response['data'];

        $wrapper = $('.swiper-wrapper');

        for (var i = 0; i < arr.length; i++) {
            $slide = $('<div></div>').addClass('swiper-slide');
            $wrapper.append($slide);

            $img = $('<img>').attr('src', arr[i]['image']);
            $slide.append($img);
        }

        var swiper = new Swiper('.swiper-container', {
            pagination: '.swiper-pagination',
            nextButton: '.swiper-button-next',
            prevButton: '.swiper-button-prev',
            slidesPerView: 1,
            paginationClickable: true,
            spaceBetween: 30,
            loop: true,
            autoplay: 1000
        });
    });

	$.getJSON('/api/v1/movie/', function (response) {
        array = response['data'];
        $movie = $('.movie_list');
        for (var i = 0; i < array.length; i++) {
            $li = $('<li></li>');
            $movie.append($li);

            $div = $('<div></div>').addClass('movie_list_left');
            $li.append($div);

            $a1 = $('<a></a>').attr('href', array[i]['request_url']).attr('title', array[i]['title']);
            $div.append($a1);

            $image = $('<img>').attr('src', array[i]['image']);
            $a1.append($image);

            $time = $('<div></div>').addClass('bottom-cover');
            $a1.append($time);

            $span = $('<span></span>').addClass('film-time').html(array[i]['duration']);
            $time.append($span);

            $div2 = $('<div></div>').addClass('movie_list_right');
            $li.append($div2);

            $h2 = $('<h2></h2>');
            $div2.append($h2);

            $a2 = $('<a></a>').attr('href', array[i]['request_url']).attr('title', array[i]['title']);
            $h2.append($a2);

            $span2 = $('<span></span>').html(array[i]['title']);
            $a2.append($span2);

            $div2_1 = $('<div></div>').addClass('movie-intro').html(array[i]['wx_small_app_title']);
            $div2.append($div2_1);

            $div2_2 = $('<div></div>').addClass('movie_like');
            $div2.append($div2_2);

            $div2_2_span_1 = $('<span></span>').addClass('glyphicon glyphicon-heart');
            $div2_2.append($div2_2_span_1);

            $div2_2_span_2 = $('<span></span>').html(array[i]['like_num']);
            $div2_2.append($div2_2_span_2);
        }
    });
});


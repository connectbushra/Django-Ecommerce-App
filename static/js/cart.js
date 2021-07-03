$(document).ready(function() {
	// Product Filter Start
	$(".filter-checkbox").on('click', function () {
		var filterObj = {};
		$(".filter-checkbox").each(function (index, ele) {
			var filterVal = $(this).val();
			var filterKey = $(this).data('filter');
			filterObj[filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + filterKey + ']:checked')).map(function (el) {
				return el.value;
			});
		});
		// // Run Ajax

		$.ajax(
			{
			url :'/filter-data',
			data:filterObj,
			dataType:'json',
	    	beforeSend:function(){
				$(".ajaxLoader").show();
			},
			success:function(res){
				console.log(res);
				$("#filteredProducts").html(res.data);
				$(".ajaxLoader").hide();
			}
		});
	});
});



// function updateUserOrder(itemId,action) {
//     console.log('user is logged in ....')
//     var url='/update_item/'
//     fetch(url,
//         {
//             method:'POST',
//             headers:{
//                 'content-Type':'application/Json'
//             },
//         })
// }
//   $('.cart').click(function () {
//                     console.log('clicked');
//             });

            /* Filtering PRoduct *********
*************************************************************


/*---------------------------  SHOW MORE  ----------------------------   */
//
// if ($('.list-group-item').length > 5) {
//   $('.list-group-item:gt(4)').hide();
//   $('.show-more').show();
// }
//
// $('.show-more').on('click', function() {
//   //toggle elements with class .list-group-item that their index is bigger than 6
//   $('.list-group-item:gt(4)').toggle();
//   $(this).text() === 'Show more....' ? $(this).text('Show less....') : $(this).text('Show less.... ');
// });

// https://dare2compete.com/quiz/20241-mcq-challenge-walmart-codehers/details
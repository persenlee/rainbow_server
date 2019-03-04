jQuery(document).ready(function($){
	//open menu
	$('.cd-menu-trigger').on('click', function(event){
		event.preventDefault();
		$('#main-content').addClass('move-out');
		$('#main-nav').addClass('is-visible');
		$('.cd-shadow-layer').addClass('is-visible');
	});
	//close menu
	$('.cd-close-menu').on('click', function(event){
		event.preventDefault();
		$('#main-content').removeClass('move-out');
		$('#main-nav').removeClass('is-visible');
		$('.cd-shadow-layer').removeClass('is-visible');
	});


    var grid = new Muuri('.grid');
    $(window).on('load', function(){
		grid.refreshItems().layout();
	});

	$(window).scroll(function(event){
	    //隐藏tag menu
	     $(".tag-menu").removeClass("showMenu");
    });



    var $container = $('.grid').infiniteScroll({
     path:  getPath,
     append: '.item',
     responseType: 'document',
     status: '.page-load-status',
     checkLastPage: true,
     debug: true
    });

    $container.on( 'append.infiniteScroll', function( event, response, path, items ) {
        //刷新瀑布流
        grid.add(items)
        grid.refreshItems().layout();
    });

    $container.on( 'error.infiniteScroll', function( event, error, path ) {
        $(".page-load-status").show()
        $(".infinite-scroll-error").show()
    });

    $container.on( 'last.infiniteScroll', function( event, response, path ) {
        $(".page-load-status").show()
        $(".infinite-scroll-last").show()
    });

   function getPath() {
        num_pages_str = $(".page-load-status").attr("num_pages")
        num_pages =parseInt(num_pages_str, 10);
        if(this.loadCount < num_pages)
            return 'image_list/?page='+(this.loadCount+2);
   }



    var initPhotoSwipeFromDOM = function(gallerySelector) {

    // parse slide data (url, title, size ...) from DOM elements
    // (children of gallerySelector)
    var parseThumbnailElements = function(el) {
        var itemElements = el.children,
            numNodes = itemElements.length,
            items = [],
            figureEl,
            linkEl,
            size,
            item;

        for(var i = 0; i < numNodes; i++) {
            itemEl =  itemElements[i];
            itemCotentEl = itemEl.children[0]; // <item-content> element

            // include only element nodes
            if(itemCotentEl.nodeType !== 1) {
                continue;
            }

            linkEl = itemCotentEl.children[0]; // <a> element


            // create slide object
            item = {
                src: linkEl.getAttribute('href'),
                w: itemCotentEl.clientWidth * 2,
                h: itemCotentEl.clientHeight * 2
            };



//            if(figureEl.children.length > 1) {
//                // <figcaption> content
//                item.title = figureEl.children[1].innerHTML;
//            }

            if(linkEl.children.length > 0) {
                // <img> thumbnail element, retrieving thumbnail url
                item.msrc = linkEl.children[0].getAttribute('src');
            }

            item.el = itemCotentEl; // save link to element for getThumbBoundsFn
            items.push(item);
        }

        return items;
    };

    // find nearest parent element
    var closest = function closest(el, fn) {
        return el && ( fn(el) ? el : closest(el.parentNode, fn) );
    };

    // triggers when user clicks on thumbnail
    var onThumbnailsClick = function(e) {
        e = e || window.event;
        e.preventDefault ? e.preventDefault() : e.returnValue = false;

        var eTarget = e.target || e.srcElement;

        var toolBarItem = closest(eTarget,function(el) {
            return (el.nodeName === 'A' &&
            (el.className === 'like' || el.className === 'tag-add'));
        });

        if(toolBarItem) {
            return;
        }

        // find root element of slide
        var clickedListItem = closest(eTarget, function(el) {
            return (el.id && el.id === 'item');
        });

        if(!clickedListItem) {
            return;
        }

        // find index of clicked item by looping through all child nodes
        // alternatively, you may define index via data- attribute
        var clickedGallery = clickedListItem.parentNode,
            childNodes = clickedGallery.childNodes,
            numChildNodes = childNodes.length,
            nodeIndex = 0,
            index;

        for (var i = 0; i < numChildNodes; i++) {
            if(childNodes[i].nodeType !== 1) {
                continue;
            }

            if(childNodes[i] === clickedListItem) {
                index = nodeIndex;
                break;
            }
            nodeIndex++;
        }



        if(index >= 0) {
            // open PhotoSwipe if valid index found
            openPhotoSwipe( index, clickedGallery );
        }
        return false;
    };

    // parse picture index and gallery index from URL (#&pid=1&gid=2)
    var photoswipeParseHash = function() {
        var hash = window.location.hash.substring(1),
        params = {};

        if(hash.length < 5) {
            return params;
        }

        var vars = hash.split('&');
        for (var i = 0; i < vars.length; i++) {
            if(!vars[i]) {
                continue;
            }
            var pair = vars[i].split('=');
            if(pair.length < 2) {
                continue;
            }
            params[pair[0]] = pair[1];
        }

        if(params.gid) {
            params.gid = parseInt(params.gid, 10);
        }

        return params;
    };

    var openPhotoSwipe = function(index, galleryElement, disableAnimation, fromURL) {
        var pswpElement = document.querySelectorAll('.pswp')[0],
            gallery,
            options,
            items;

        items = parseThumbnailElements(galleryElement);

        // define options (if needed)
        options = {

            // define gallery index (for URL)
            galleryUID: galleryElement.getAttribute('data-pswp-uid'),

            getThumbBoundsFn: function(index) {
                // See Options -> getThumbBoundsFn section of documentation for more info
                var thumbnail = items[index].el.getElementsByTagName('img')[0], // find thumbnail
                    pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
                    rect = thumbnail.getBoundingClientRect();

                return {x:rect.left, y:rect.top + pageYScroll, w:rect.width};
            }

        };

        // PhotoSwipe opened from URL
        if(fromURL) {
            if(options.galleryPIDs) {
                // parse real index when custom PIDs are used
                // http://photoswipe.com/documentation/faq.html#custom-pid-in-url
                for(var j = 0; j < items.length; j++) {
                    if(items[j].pid == index) {
                        options.index = j;
                        break;
                    }
                }
            } else {
                // in URL indexes start from 1
                options.index = parseInt(index, 10) - 1;
            }
        } else {
            options.index = parseInt(index, 10);
        }

        // exit if index not found
        if( isNaN(options.index) ) {
            return;
        }

        if(disableAnimation) {
            options.showAnimationDuration = 0;
        }

        // Pass data to PhotoSwipe and initialize it
        gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
    };

    // loop through all gallery elements and bind events
    var galleryElements = document.querySelectorAll( gallerySelector );

    for(var i = 0, l = galleryElements.length; i < l; i++) {
        galleryElements[i].setAttribute('data-pswp-uid', i+1);
        galleryElements[i].onclick = onThumbnailsClick;
    }

    // Parse URL and open gallery if it contains #&pid=3&gid=1
    var hashData = photoswipeParseHash();
    if(hashData.pid && hashData.gid) {
        openPhotoSwipe( hashData.pid ,  galleryElements[ hashData.gid - 1 ], true, true );
    }
};

// execute above function
initPhotoSwipeFromDOM('.grid');


$(".grid").on("click",".like",function(e){
    e.preventDefault(); // cancel the link itself
    var aNode = e.currentTarget;
    var image_id = aNode.getAttribute('image-value');
    var like = aNode.getAttribute('like-value');
    like = parseInt(like) ? 0 : 1;
    $.ajax({
        type: "GET", // 使用post方式
        url: "star/",
        data: {"star": like,"image_id":image_id}, // 参数列表，stringify()方法用于将JS对象序列化为json字符串
        success: function(result){
            if(result.status == 1) {
                var imageNode = aNode.children[0];
                var add_css = like ? 'like-on' : 'like-off';
                var remove_css = like ? 'like-off' : 'like-on';

                imageNode.classList.remove(remove_css);
                imageNode.classList.add(add_css);

                var spanNode = aNode.parentNode.children[1];
                var likeCount =  parseInt(spanNode.innerText);
                var likeAfter = Math.max((like ? likeCount + 1 : likeCount - 1),0);
                spanNode.innerText = likeAfter;

                aNode.setAttribute('like-value',like);

            } else if(result.status == 0) {
            } else if(result.status == -101) {
                login_url = window.location.protocol + "//"+window.location.host + '/user'
                $(location).attr('href', login_url);
            }
        },
        error: function(result){
        // 请求失败后的操作
            alert('')
        }
    });
})

$(".grid").on("click",".tag-add",function(e){
     e.preventDefault();
     $(".tag-menu").toggleClass("showMenu");
     var tagAddNode = e.currentTarget;
     var imageNode = tagAddNode.parentNode.children[0];
     var tagListNode = tagAddNode.parentNode.children[2];
     var image_id = imageNode.getAttribute('image-value');
     $(".tag-menu > li").click(function(e){
        var tagNode = e.currentTarget;
        var tag_id = tagNode.getAttribute('id-value');
        var tag_name = tagNode.innerText;
        $.ajax({
            type: 'POST',
            url: 'add_tag/',
            data: {"tag_id": tag_id,"image_id":image_id}, // 参数列表，stringify()方法用于将JS对象序列化为json字符串
        success: function(result){
            if(result.status == 1) {
                var tag = document.querySelector('#tag');
                tag.content.querySelector('li').setAttribute('id-value',tag_id);
                tag.content.querySelector('a').innerHTML = tag_name;
                tagListNode.appendChild(tag.content.cloneNode(true));
            } else if(result.status == 0) {

            }
        },
        error: function(result){
        // 请求失败后的操作
            alert('服务器错误')
        }
        })

        $(".tag-menu").removeClass("showMenu");
     });
  })

})


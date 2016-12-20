/* @flow */

import 'bootstrap-sass'
import $ from 'jquery'
import 'jquery.cookie'

import '../scss/storefront.scss'

let csrftoken = $.cookie('csrftoken')

function csrfSafeMethod(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken)
    }
  }
})

$(function() {
  const $carousel = $('.carousel')
  const $items = $('.product-gallery-item')
  const $modal = $('.modal')

  $items.on('click', function(e) {
    if ($carousel.is(':visible')) {
      e.preventDefault()
    }
    const index = $(this).index()
    $carousel.carousel(index)
  })

  $modal.on('show.bs.modal', function() {
    const $img = $(this).find('.modal-body img')
    const dataSrc = $img.attr('data-src')
    $img.attr('src', dataSrc)
  })
})

$(function() {
  const $i18nAddresses = $('.i18n-address')
  $i18nAddresses.each(function () {
    const $form = $(this).closest('form')
    const $countryField = $form.find('select[name=country]')
    const $previewField = $form.find('input.preview')
    $countryField.on('change', () => {
      $previewField.val('on')
      $form.submit()
    })
  })
})

// jQuery for page scrolling feature - requires jQuery Easing plugin
$('a.page-scroll').bind('click', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
        scrollTop: ($($anchor.attr('href')).offset().top - 50)
    }, 1250, 'easeInOutExpo');
    event.preventDefault();
});

$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

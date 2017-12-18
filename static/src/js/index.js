/* global window document */
window.jQuery = window.$ = require('jquery');

const $ = window.$;

require('bootstrap/dist/js/bootstrap.bundle');
require('bootstrap-slider');

import ajaxSendMethod from './ajax';
import handleMessageDismiss from './messages';
import loadStripeElements from './pinax-stripe';
import hookupCustomFileWidget from './pinax-documents';

$(() => {
    $(document).ajaxSend(ajaxSendMethod);

    // Topbar active tab support
    $('.topbar li').removeClass('active');

    const classList = $('body').attr('class').split(/\s+/);
    $.each(classList, (index, item) => {
        const selector = `ul.nav li#tab_${item}`;
        $(selector).addClass('active');
    });

    $('#account_logout, .account_logout').click(e => {
        e.preventDefault();
        $('#accountLogOutForm').submit();
    });

    $('#freq-filt-slider').slider({
      id: 'frequency-filter-slider',
      range: true,
      value: [0, 8],
      ticks: [0, 1, 2, 3, 4, 5, 6, 7, 8],
      ticks_labels: ['', 0.1, 0.2, 0.5, 1, 2, 5, 10, ''],
      tooltip: 'hide',
    });

    handleMessageDismiss();
    loadStripeElements();
    hookupCustomFileWidget();
});

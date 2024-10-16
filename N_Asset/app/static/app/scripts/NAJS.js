if (typeof NA == "undefined") window.NA = {}
NA.NAEvent = {
  doc: window.document,
  addHandler: function (element, type, handler) {
    if (element.addEventListener) {
      element.addEventListener(type, handler, false);
    } else if (element.attachEvent) {
      element.attachEvent("on" + type, handler);
    } else {
      element["on" + type] = handler;
    }
  },
  // events and args should be of type Array
  addMultipleListeners: function (element, events, handler, useCapture, args) {
    if (!(events instanceof Array)) {
      throw 'addMultipleListeners: ' +
      'please supply an array of eventstrings ' +
      '(like ["click","mouseover"])';
    }
    //create a wrapper to be able to use additional arguments
    var handlerFn = function (e) {
      handler.apply(this, args && args instanceof Array ? args : []);
    }
    for (var i = 0; i < events.length; i += 1) {
      element.addEventListener(events[i], handlerFn, useCapture);
    }
  },
  getButton: function (event) {
    if (this.doc.implementation.hasFeature("MouseEvents", "2.0")) {
      return event.button;
    } else {
      switch (event.button) {
        case 0:
        case 1:
        case 3:
        case 5:
        case 7:
          return 0;
        case 2:
        case 6:
          return 2;
        case 4:
          return 1;
      }
    }
  },
  getCharCode: function (event) {
    if (typeof event.charCode == "number") {
      return event.charCode;
    } else {
      return event.keyCode;
    }
  },
  getClipboardText: function (event) {
    var clipboardData = (event.clipboardData || window.clipboardData);
    return clipboardData.getData("text");
  },
  getEvent: function (event) {
    return event ? event : window.event;
  },
  getRelatedTarget: function (event) {
    if (event.relatedTarget) {
      return event.relatedTarget;
    } else if (event.toElement) {
      return event.toElement;
    } else if (event.fromElement) {
      return event.fromElement;
    } else {
      return null;
    }
  },
  getTarget: function (event) {
    return event.target || event.srcElement;
  },
  getWheelDelta: function (event) {
    if (event.wheelDelta) {
      return (client.engine.opera && client.engine.opera < 9.5 ? -event.wheelDelta : event.wheelDelta);
    } else {
      return -event.detail * 40;
    }
  },
  preventDefault: function (event) {
    if (event.preventDefault) {
      event.preventDefault();
    } else {
      event.returnValue = false;
    }
  },
  removeHandler: function (element, type, handler) {
    if (element.removeEventListener) {
      element.removeEventListener(type, handler, false);
    } else if (element.detachEvent) {
      element.detachEvent("on" + type, handler);
    } else {
      element["on" + type] = null;
    }
  },
  setClipboardText: function (event, value) {
    if (event.clipboardData) {
      event.clipboardData.setData("text/plain", value);
    } else if (window.clipboardData) {
      window.clipboardData.setData("text", value);
    }
  },
  stopPropagation: function (event) {
    if (event.stopPropagation) {
      event.stopPropagation();
    } else {
      event.cancelBubble = true;
    }
  }
};
//=====================COOKIE Utility==========================
NA.CookieUtil = {
  doc: window.document,
  get: function (name) {
    var cookieName = encodeURIComponent(name) + "=",
      cookieStart = this.doc.cookie.indexOf(cookieName),
      cookieValue = null,
      cookieEnd;
    if (cookieStart > -1) {
      cookieEnd = this.doc.cookie.indexOf(";", cookieStart);
      if (cookieEnd == -1) {
        cookieEnd = this.doc.cookie.length;
      }
      cookieValue = decodeURIComponent(this.doc.cookie.substring(cookieStart + cookieName.length, cookieEnd));
    }
    return cookieValue;
  },
  set: function (name, value, expires, path, domain, secure) {
    var cookieText = encodeURIComponent(name) + "=" + encodeURIComponent(value);
    if (expires instanceof Date) {
      cookieText += "; expires=" + expires.toGMTString();
    }
    if (path) {
      cookieText += "; path=" + path;
    }
    if (domain) {
      cookieText += "; domain=" + domain;
    }
    if (secure) {
      cookieText += "; secure";
    }
    this.doc.cookie = cookieText;
  },
  unset: function (name, path, domain, secure) {
    this.set(name, "", new Date(0), path, domain, secure);
  }
};
//====================Client Utility===========================================
NA.client = function () {
  //rendering engines
  var engine = {
    ie: 0,
    gecko: 0,
    webkit: 0,
    khtml: 0,
    opera: 0,
    //complete version
    ver: null
  };
  //browsers
  var browser = {
    //browsers
    ie: 0,
    firefox: 0,
    safari: 0,
    konq: 0,
    opera: 0,
    chrome: 0,
    //specific version
    ver: null
  };
  //platform/device/OS
  var system = {
    win: false,
    mac: false,
    x11: false,
    //mobile devices
    iphone: false,
    ipod: false,
    ipad: false,
    ios: false,
    android: false,
    nokiaN: false,
    winMobile: false,
    //game systems
    wii: false,
    ps: false
  };
  var url = {
    login_next: (function () {
      var current_url = window.location.href.replace(window.location.origin, '')
      return "/login/?next=" + current_url
    })()
  }
  //detect rendering engines/browsers
  var ua = "Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0) Asus;Galaxy6"; //navigator.userAgent;
  if (window.opera) {
    engine.ver = browser.ver = window.opera.version();
    engine.opera = browser.opera = parseFloat(engine.ver);
  } else if (/AppleWebKit\/(\S+)/.test(ua)) {
    engine.ver = RegExp["$1"];
    engine.webkit = parseFloat(engine.ver);
    //figure out if it's Chrome or Safari
    if (/Chrome\/(\S+)/.test(ua)) {
      browser.ver = RegExp["$1"];
      browser.chrome = parseFloat(browser.ver);
    } else if (/Version\/(\S+)/.test(ua)) {
      browser.ver = RegExp["$1"];
      browser.safari = parseFloat(browser.ver);
    } else {
      //approximate version
      var safariVersion = 1;
      if (engine.webkit < 100) {
        safariVersion = 1;
      } else if (engine.webkit < 312) {
        safariVersion = 1.2;
      } else if (engine.webkit < 412) {
        safariVersion = 1.3;
      } else {
        safariVersion = 2;
      }
      browser.safari = browser.ver = safariVersion;
    }
  } else if (/KHTML\/(\S+)/.test(ua) || /Konqueror\/([^;]+)/.test(ua)) {
    engine.ver = browser.ver = RegExp["$1"];
    engine.khtml = browser.konq = parseFloat(engine.ver);
  } else if (/rv:([^\)]+)\) Gecko\/\d{8}/.test(ua)) {
    engine.ver = RegExp["$1"];
    engine.gecko = parseFloat(engine.ver);
    //determine if it's Firefox
    if (/Firefox\/(\S+)/.test(ua)) {
      browser.ver = RegExp["$1"];
      browser.firefox = parseFloat(browser.ver);
    }
  } else if (/MSIE ([^;]+)/.test(ua)) {
    engine.ver = browser.ver = RegExp["$1"];
    engine.ie = browser.ie = parseFloat(engine.ver);
  }
  //detect browsers
  browser.ie = engine.ie;
  browser.opera = engine.opera;
  //detect platform
  var p = navigator.platform;
  system.win = p.indexOf("Win") == 0;
  system.mac = p.indexOf("Mac") == 0;
  system.x11 = (p == "X11") || (p.indexOf("Linux") == 0);
  //detect windows operating systems
  if (system.win) {
    if (/Win(?:dows )?([^do]{2})\s?(\d+\.\d+)?/.test(ua)) {
      if (RegExp["$1"] == "NT") {
        switch (RegExp["$2"]) {
          case "5.0":
            system.win = "2000";
            break;
          case "5.1":
            system.win = "XP";
            break;
          case "6.0":
            system.win = "Vista";
            break;
          case "6.1":
            system.win = "7";
            break;
          default:
            system.win = "NT";
            break;
        }
      } else if (RegExp["$1"] == "9x") {
        system.win = "ME";
      } else {
        system.win = RegExp["$1"];
      }
    }
  }
  //mobile devices
  system.iphone = ua.indexOf("iPhone") > -1;
  system.ipod = ua.indexOf("iPod") > -1;
  system.ipad = ua.indexOf("iPad") > -1;
  system.nokiaN = ua.indexOf("NokiaN") > -1;
  //windows mobile
  if (system.win == "CE") {
    system.winMobile = system.win;
  } else if (system.win == "Ph") {
    if (/Windows Phone OS (\d+.\d+)/.test(ua)) {
      ;
      system.win = "Phone";
      system.winMobile = parseFloat(RegExp["$1"]);
    }
  }
  //determine iOS version
  if (system.mac && ua.indexOf("Mobile") > -1) {
    if (/CPU (?:iPhone )?OS (\d+_\d+)/.test(ua)) {
      system.ios = parseFloat(RegExp.$1.replace("_", "."));
    } else {
      system.ios = 2; //can't really detect - so guess
    }
  }
  //determine Android version
  if (/Android (\d+\.\d+)/.test(ua)) {
    system.android = parseFloat(RegExp.$1);
  }
  //gaming systems
  system.wii = ua.indexOf("Wii") > -1;
  system.ps = /playstation/i.test(ua);
  //return it
  return {
    engine: engine,
    browser: browser,
    browserName: (function () {
      if (navigator.userAgent.indexOf("Edge") > -1 && navigator.appVersion.indexOf('Edge') > -1) {
        return 'Edge';
      } else if (navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf('OPR') != -1) {
        return 'Opera';
      } else if (navigator.userAgent.indexOf("Chrome") != -1) {
        return 'Chrome';
      } else if (navigator.userAgent.indexOf("Safari") != -1) {
        return 'Safari';
      } else if (navigator.userAgent.indexOf("Firefox") != -1) {
        return 'Firefox';
      } else if ((navigator.userAgent.indexOf("MSIE") != -1) || (!!document.documentMode == true)) //IF IE > 10
      {
        return 'IE';
      } else {
        return 'unknown';
      }
    })(),
    system: system,
    url: url
  };
}();
NA.common = {
  //assign Object cross browser
  AssignObject: function () {
    var resObj = {};
    for (var i = 0; i < arguments.length; i++) {
      var obj = arguments[i],
        keys = Object.keys(obj);
      for (var j = 0; j < keys.length; j++) {
        resObj[keys[j]] = obj[keys[j]];
      }
    }
    return resObj; //result Object
  },
  doc: window.document,
  //============Validate Input Number========================
  numberInput: function (evt) {
    var e = NA.NAEvent.getEvent(evt);
    var key = e.keyCode || e.which;
    if (!e.shiftKey && !e.altKey && !e.ctrlKey &&
      // numbers
      key >= 48 && key <= 57 ||
      // Numeric keypad
      key >= 96 && key <= 105) {
      // input is VALID
      return true;
    } else {
      // input is INVALID
      if (
        // Backspace and Tab and Enter by pass
        key == 8 || key == 9 || key == 13 ||
        // Home and End
        key == 35 || key == 36 ||
        // left and right arrows
        key == 37 || key == 39 ||
        // Del and Ins
        key == 46 || key == 45) { return true; }
      key = String.fromCharCode(key);
      var regex = /[0-9]/;
      return regex.test(key);
    }
  },
  //============CROSS BROWSER Keyboard event====================
  triggerKeyboardEvent: function (el, keyCode) {
    if (NA.client.browserName == "Chrome") {
      var event = document.createEvent('Event');
      event.initEvent('keydown', true, true);
      event.keyCode = keyCode;
      el.dispatchEvent(event);
    } else {
      var keyboardEvent = document.createEvent("KeyboardEvent");
      var initMethod = typeof keyboardEvent.initKeyboardEvent !== 'undefined' ? "initKeyboardEvent" : "initKeyEvent";
      keyboardEvent[initMethod]("keydown", false, // bubbles oOooOOo0
        true, // cancelable
        window, // view
        false, // ctrlKeyArg
        false, // altKeyArg
        false, // shiftKeyArg
        false, // metaKeyArg
        keyCode, 0 // charCode
      );
      el.dispatchEvent(keyboardEvent);
    }
  },
  //===========cross browser get Element ByID =====================
  getElementID: function (id) {
    if (this.doc.getElementById) {
      return this.doc.getElementById(id);
    } else if (this.doc.all) {
      return this.doc.all[id];
    } else {
      throw new Error("No way to retrieve element!");
    }
  },
  //============cross browser getquerystring arguments==============
  getQueryStringArgs: function () {
    //get query string without the initial ?
    var qs = (location.search.length > 0 ? location.search.substring(1) : ""),
      //object to hold data
      args = {},
      //get individual items
      items = qs.length ? qs.split("&") : [],
      item = null,
      name = null,
      value = null,
      //used in for loop
      i = 0,
      len = items.length;
    //assign each item onto the args object
    for (i = 0; i < len; i++) {
      item = items[i].split("=");
      name = decodeURIComponent(item[0]);
      value = decodeURIComponent(item[1]);
      if (name.length) {
        args[name] = value;
      }
    }
    return args;
  },
  //==============Load Dinamic Script============================
  loadScript: function (url, Elem, id) {
    var script = this.doc.createElement("script");
    script.type = "text/javascript";
    script.src = url;
    script.setAttribute('id', id)
    if (id) {
      if (this.doc.querySelector(id) != 'undefined') {
        if (typeof (Elem) == 'undefined') {
          this.doc.body.appendChild(script)
        } else {
          Elem.appendChild(script)
        }
      }
    } else {
      if (typeof (Elem) == 'undefined') {
        this.doc.body.appendChild(script)
      } else {
        Elem.appendChild(script)
      }
    }
  },
  //=============Load Dynamic Style=======================
  loadStyles: function (url, id) {
    var link = this.doc.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = url;
    if (id) {
      link.setAttribute('id', id)
      if (this.doc.querySelector(id) != 'undefined') {
        var head = this.doc.getElementsByTagName("header")[0];
        head.appendChild(link);
      }
    } else {
      var head = this.doc.getElementsByTagName("header")[0];
      head.appendChild(link);
    }
  },
  //==================Retrieving Selected Text======================
  getSelectedText: function (textbox, startIndex, stopIndex) {
    if (textbox.setSelectionRange) {
      textbox.setSelectionRange(startIndex, stopIndex);
    } else if (textbox.createTextRange) {
      var range = textbox.createTextRange();
      range.collapse(true);
      range.moveStart("character", startIndex);
      range.moveEnd("character", stopIndex - startIndex);
      range.select();
    }
    textbox.focus();
  },
  //===============ENCODE URL=================================
  addURLParam: function (url, name, value) {
    url += (url.indexOf("?") == -1 ? "?" : "&");
    url += encodeURIComponent(name) + "=" + encodeURIComponent(value);
    return url;
  },
  //================== CONVERT Object to Array ====================
  //================== CONVERT Object to Array ====================
  objectToArray: function (obj) {
    var _arr = [];
    for (var key in obj) {
      _arr.push([key, obj[key]]);
    }
    return _arr;
  },
  //function ini untuk mengecek apakah object bernilai {}, jika object ada key/method/isinya maka return false
  isObjectEmpty: function (obj) {
    for (var x in obj) {
      if (obj.hasOwnProperty(x)) return false;
    }
    return true;
  },
  removeQuotes: function (str) {
    return str.replace(/["]+/g, '')
  },
  //=================calculate months with date ============================
  addMonths: function (date, months) {
    var result = new Date(date);
    var expectedMonth = ((result.getMonth() + months) % 12 + 12) % 12;
    result.setMonth(result.getMonth() + months);
    if (result.getMonth() !== expectedMonth) {
      result.setDate(0);
    }
    return result;
  },
  GetServerFormatDate: function (parsedDate) { //dd/mm/yy value -->yyyy-mm-dd
    var d = new Date(parsedDate),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();
    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;
    return [year, month, day].join('-');
  },
  //addDate: function (date, dates) {
  //    var result = new Date(date);
  //    var expectedDate = ((result.getDate() + dates) % 12 + 12) % 12;
  //    result.setMonth(result.getMonth() + months);
  //    if (result.getMonth() !== expectedMonth) {
  //        result.setDate(0);
  //    }
  //    return result;
  //},
  FormatNumber: function (num, decimals, dec_point, thousands_sep) {
    NNum = 0;
    if (typeof num === 'string') {
      NNum = Number(num.trim());
    } else {
      NNum = Number(num)
    }
    dec_point = typeof dec_point !== 'undefined' ? dec_point : '.';
    thousands_sep = typeof thousands_sep !== 'undefined' ? thousands_sep : ',';
    var parts = NNum.toFixed(decimals).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousands_sep);
    if (NNum <= 0 || NNum === '0') {
      return String(NNum) + dec_point + '00';
    }
    return parts.join(dec_point);
  },
  //=======================FORM SERIALIZATION==========================
  serializeForm: function (form) {
    var parts = [],
      field = null,
      i,
      len,
      j,
      optLen,
      option,
      optValue;
    for (i = 0, len = form.elements.length; i < len; i++) {
      field = form.elements[i];
      switch (field.type) {
        case "select-one":
        case "select-multiple":
          if (field.name.length) {
            for (j = 0, optLen = field.options.length; j < optLen; j++) {
              option = field.options[j];
              if (option.selected) {
                optValue = "";
                if (option.hasAttribute) {
                  optValue = (option.hasAttribute("value") ? option.value : option.text);
                } else {
                  optValue = (option.attributes["value"].specified ? option.value : option.text);
                }
                parts.push(encodeURIComponent(field.name) + "=" + encodeURIComponent(optValue));
              }
            }
          }
          break;
        case undefined: //fieldset
        case "file": //file input
        case "submit": //submit button
        case "reset": //reset button
        case "button": //custom button
          break;
        case "radio": //radio button
        case "checkbox": //checkbox
          if (!field.checked) {
            break;
          }
        /* falls through */
        default:
          //don’t include form fields without names
          if (field.name.length) {
            parts.push(encodeURIComponent(field.name) + "=" + encodeURIComponent(field.value));
          }
      }
    }
    return parts.join("&");
  },
  //sebelum di compare objForm mesti di trim spacenya
  detectInputChanges: function (JsonObjInitialize, JsonObjSerializeForm) {
    var a = JSON.stringify(JsonObjInitialize),
      b = JSON.stringify(JsonObjSerializeForm);
    return (a.split('').sort().join('') !== b.split('').sort().join(''));
  },
  //function untuk mendisable kan element form
  //parameter form = document.form[0]/form_id
  //parameter typeofElements = type element apa saja yang akan di disabledkan
  disableForm: function (form, typeofElements) {
    var length = form.elements.length,
      i;
    for (i = 0; i < length; i++) {
      var elementType = form.elements[i].type;
      if (typeofElements) {
        if (typeofElements.indexOf(elementType) > -1) {
          //form.elements[i].setAttribute('disabled', 'true')
          form.elements[i].disabled = true;
        }
      } else {
        if (elementType === 'text' || elementType === 'textarea' || elementType === 'select' || elementType === 'checkbox') {
          form.elements[i].disabled = true;
        }
      }
    }
  },
  SearchData: function () {
    var elSearch = elSearch || window.document.querySelector('li.dropdown>a#bySearch');
    //valueKey   = NA.common.doc.querySelector('li.dropdown>a#bySearch').textContent.trim();
    var valueKey = ''; //valueKey === 'By'?'':valueKey;
    var columnKey = ''; //elSearch.dataset.column ? elSearch.dataset.column : 'goodsname';
    var dataType = ''; //;elSearch.dataset.column ? elSearch.dataset.tipe : 'Varchar';
    var criteria = 'like';
    return {
      //==========setDefault value=================================
      setDefaultSearchData: function (defaultColumn, defaultDataType, defaultCriteria) {
        this.columnKey = defaultColumn;
        this.dataType = defaultDataType;
        this.criteria = defaultCriteria;
        this.valueKey = '';
      },
      //==========getter===============
      getValueKey: function () {
        return this.valueKey;
      },
      getColumnKey: function () {
        return this.columnKey;
      },
      getDataType: function () {
        return this.dataType;
      },
      getCriteria: function () {
        return this.criteria;
      },
      //==========setter=================
      setValue: function (nValue) {
        this.valueKey = nValue;
      },
      setColumnName: function (ncolKey) {
        this.columnKey = ncolKey;
      },
      setDataType: function (nDataType) {
        this.dataType = nDataType;
      },
      setCriteria: function (nCriteria) {
        this.criteria = nCriteria;
      },
    }
  }(),
  NA_setAttr: function (el, attrs) {
    for (var key in attrs) {
      el.setAttribute(key, attrs[key]);
    }
  },
  qs: function (el) {
    if (typeof NA.common.doc.querySelector !== "undefined") {
      return NA.common.doc.querySelector(el);
    } else {
      throw new Error("No way to retrieve element!");
    }
  },
  qsAll: function (el) {
    if (typeof NA.common.doc.querySelectorAll !== "undefined") {
      return NA.common.doc.querySelectorAll(el);
    } else {
      throw new Error("No way to retrieve element!");
    }
  },
};
NA.common.dialog = {
  doc: window.document,
  getPageDimensions: function () {
    var body = this.doc.getElementsByTagName("body")[0];
    var bodyOffsetWidth = 0;
    var bodyOffsetHeight = 0;
    var bodyScrollWidth = 0;
    var bodyScrollHeight = 0;
    var pageDimensions = [0, 0];
    if (typeof this.doc.documentElement != "undefined" && typeof this.doc.documentElement.scrollWidth != "undefined") {
      pageDimensions[0] = this.doc.documentElement.scrollWidth;
      pageDimensions[1] = this.doc.documentElement.scrollHeight;
    }
    bodyOffsetWidth = body.offsetWidth;
    bodyOffsetHeight = body.offsetHeight;
    bodyScrollWidth = body.scrollWidth;
    bodyScrollHeight = body.scrollHeight;
    if (bodyOffsetWidth > pageDimensions[0]) {
      pageDimensions[0] = bodyOffsetWidth;
    }
    if (bodyOffsetHeight > pageDimensions[1]) {
      pageDimensions[1] = bodyOffsetHeight;
    }
    if (bodyScrollWidth > pageDimensions[0]) {
      pageDimensions[0] = bodyScrollWidth;
    }
    if (bodyScrollHeight > pageDimensions[1]) {
      pageDimensions[1] = bodyScrollHeight;
    }
    return pageDimensions;
  },
  getViewportSize: function () {
    var size = [0, 0];
    if (typeof window.innerWidth != 'undefined') {
      size = [
        window.innerWidth,
        window.innerHeight
      ];
    } else if (typeof this.doc.documentElement != 'undefined' && typeof this.doc.documentElement.clientWidth != 'undefined' && this.doc.documentElement.clientWidth != 0) {
      size = [
        this.doc.documentElement.clientWidth,
        this.doc.documentElement.clientHeight
      ];
    } else {
      size = [
        this.doc.getElementsByTagName('body')[0].clientWidth,
        this.doc.getElementsByTagName('body')[0].clientHeight
      ];
    }
    return size;
  },
  getScrollingPosition: function () {
    var position = [0, 0];
    if (typeof window.pageYOffset != 'undefined') {
      position = [
        window.pageXOffset,
        window.pageYOffset
      ];
    } else if (typeof this.doc.documentElement.scrollTop != 'undefined' && this.doc.documentElement.scrollTop > 0) {
      position = [
        this.doc.documentElement.scrollLeft,
        this.doc.documentElement.scrollTop
      ];
    } else if (typeof this.doc.body.scrollTop != 'undefined') {
      position = [
        this.doc.body.scrollLeft,
        this.doc.body.scrollTop
      ];
    }
    return position;
  },
  createFormContainer: function (IDForControl, placeHolderForSearch, handlerForBlurSearch, HandlerForFocusSearch, HandlerForKeyDown, handlerbtnSearch) {
    var containerForm = this.doc.createElement("div");
    containerForm.className = 'containerForm';
    containerForm.classList.add(IDForControl);
    containerForm.style.cssText = 'margin:auto;';
    //create Header for Searching
    var HeaderSearching = this.doc.createElement('div');
    HeaderSearching.setAttribute('style', 'width:99%');
    HeaderSearching.className = 'input-group';
    //     <div class="input-group">
    //  <input type="text" class="form-control" placeholder="Search" name="search">
    //  <div class="input-group-btn">
    //    <button class="btn btn-default" type="submit"><i class="glyphicon glyphicon-search"></i></button>
    //  </div>
    //</div>
    //create TextBox Searching with placeholder
    var searchText = this.doc.createElement('input');
    searchText.type = 'text';
    searchText.className = 'NA-Form-Control';
    searchText.classList.add(IDForControl);
    searchText.style.cssText = 'border-radius:0';
    searchText.id = 'txtsearch_' + IDForControl;
    searchText.setAttribute('placeholder', placeHolderForSearch);
    if (handlerForBlurSearch) {
      NA.NAEvent.addHandler(searchText, 'blur', handlerForBlurSearch);
    }
    if (HandlerForFocusSearch) {
      NA.NAEvent.addHandler(searchText, 'focus', HandlerForFocusSearch);
    }
    if (HandlerForKeyDown) {
      NA.NAEvent.addHandler(searchText, 'keydown', HandlerForKeyDown);
    }
    var inputGrButton = this.doc.createElement('div');
    inputGrButton.className = 'input-group-btn';
    var btnSearch = this.doc.createElement('button');
    btnSearch.className = 'btn';
    btnSearch.classList.add('btn-success');
    btnSearch.type = 'button';
    var Iicon = this.doc.createElement('i');
    Iicon.className = 'glyphicon';
    Iicon.classList.add('glyphicon-search');
    btnSearch.appendChild(Iicon);
    btnSearch.style.height = '27px';
    if (handlerbtnSearch) {
      NA.NAEvent.addHandler(btnSearch, 'click', handlerbtnSearch);
    }
    inputGrButton.appendChild(btnSearch);
    HeaderSearching.appendChild(searchText);
    HeaderSearching.appendChild(inputGrButton);
    var mainContainer = this.doc.createElement('div');
    mainContainer.className = 'maincontainerForm';
    mainContainer.style.cssText = 'overflow-x:auto;';
    mainContainer.classList.add(IDForControl);
    containerForm.appendChild(HeaderSearching);
    containerForm.appendChild(mainContainer);
    return containerForm;
  },
  createSearchDialog: function (event, args) {
    var body = this.doc.body;
    var pageDimensions = this.getPageDimensions();
    var viewportSize = this.getViewportSize();
    if (viewportSize[1] > pageDimensions[1]) {
      pageDimensions[1] = viewportSize[1];
    }
    var mnuContainer = this.doc.querySelector('nav.navbar.navbar-default')
    if (mnuContainer) {
      mnuContainer.style.zIndex = "0";
    }
    var dropSheet = this.doc.createElement("div");
    dropSheet.setAttribute("id", "dropSheet");
    dropSheet.style.position = "absolute";
    dropSheet.style.left = "0";
    dropSheet.style.top = "0";
    dropSheet.style.zIndex = 1;
    dropSheet.style.width = pageDimensions[0] + "px";
    dropSheet.style.height = pageDimensions[1] + "px";
    body.appendChild(dropSheet);
    var dialog = this.doc.querySelector("div.containerDialog");
    if (!dialog) {
      dialog = this.doc.createElement("div");
      dialog.className = 'containerDialog';
      dialog.style.padding = '0px'
      //dialog.classList.add("draggable");
    }
    dialog.style.visibility = "hidden";
    dialog.style.position = "absolute";
    dialog.style.zIndex = "2";
    var scrollingPosition = this.getScrollingPosition();
    body.appendChild(dialog);
    dialog.style.left = scrollingPosition[0] + parseInt(viewportSize[0] / 3) - parseInt(dialog.offsetWidth / 2) + "px";
    dialog.style.top = scrollingPosition[1] + parseInt(viewportSize[1] / 2.5) - parseInt(dialog.offsetHeight) + "px";
    dialog.style.visibility = 'visible';
    //trigger showDialogEntry
    window.showDialogCustomSearch(event);
    //===============Enabled kan Dragdrop=================================
    NA.common.dialog.DragDrop.enable();
  },
  createDialog: function (event, args) {
    var body = this.doc.body;
    var pageDimensions = this.getPageDimensions();
    var viewportSize = this.getViewportSize();
    if (viewportSize[1] > pageDimensions[1]) {
      pageDimensions[1] = viewportSize[1];
    }
    var mnuContainer = this.doc.querySelector('nav.navbar.navbar-default')
    if (mnuContainer) {
      mnuContainer.style.zIndex = "0";
    }
    var dropSheet = this.doc.createElement("div");
    dropSheet.setAttribute("id", "dropSheet");
    dropSheet.style.position = "absolute";
    dropSheet.style.left = "0";
    dropSheet.style.top = "0";
    dropSheet.style.zIndex = 1;
    dropSheet.style.width = pageDimensions[0] + "px";
    dropSheet.style.height = pageDimensions[1] + "px";
    body.appendChild(dropSheet);
    try {
      var dialog = this.doc.querySelector("div.containerDialog");
      if (!dialog) {
        dialog = this.doc.createElement("div");
        dialog.className = 'containerDialog';
      }
      //dialog.classList.add("draggable");
      dialog.style.visibility = "hidden";
      dialog.style.position = "absolute";
      dialog.style.zIndex = "2";
      //=============create Header Dialog======================
      var headerDialog = this.doc.createElement("div");
      headerDialog.className = "ui-dialog-titlebar"
      headerDialog.classList.add("ui-corner-all");
      headerDialog.classList.add("ui-widget-header");
      headerDialog.classList.add("ui-helper-clearfix");
      headerDialog.classList.add("ui-draggable-handle");
      headerDialog.classList.add("draggable");
      headerDialog.style.cursor = 'move'
      //create Span element
      var spanDialogTitle = this.doc.createElement('span');
      spanDialogTitle.setAttribute('id', 'ui-id-18');
      spanDialogTitle.className = "ui-dialog-title";
      //get title value from parameter
      var dialogTitle = args['dialogTitle'];
      spanDialogTitle.textContent = dialogTitle || "Nufarm Entry Data";
      //create button element
      var dialogCloseButton = this.doc.createElement("button");
      dialogCloseButton.className = "ui-button";
      dialogCloseButton.classList.add("ui-corner-all");
      dialogCloseButton.classList.add("ui-widget");
      dialogCloseButton.classList.add("ui-button-icon-only");
      dialogCloseButton.classList.add("ui-dialog-titlebar-close");
      dialogCloseButton.style.cssFloat = "right";
      dialogCloseButton.style.marginTop = "3px";
      dialogCloseButton.style.paddingLeft = ".5em";
      dialogCloseButton.style.paddingRight = ".5em"
      //create element spanDialogbutton close
      var spandialogbuttonclose = this.doc.createElement("span");
      spandialogbuttonclose.className = "ui-button-icon";
      spandialogbuttonclose.classList.add("ui-icon");
      spandialogbuttonclose.classList.add("ui-icon-closethick");
      var spanuibuttonIconSpace = this.doc.createElement("span");
      spanuibuttonIconSpace.className = "ui-button-icon-space";
      dialogCloseButton.appendChild(spanuibuttonIconSpace);
      dialogCloseButton.appendChild(spandialogbuttonclose);
      headerDialog.appendChild(spanDialogTitle);
      headerDialog.appendChild(dialogCloseButton); //1
      //===============create maincontendialog===============
      var mainContentDialog = this.doc.createElement("div");
      mainContentDialog.className = "maindialogContent"; //2
      //isi content di loag pakai ajax Jquery(diluar object ini) setelah dialog di create
      //=============create bottom dialog=====================
      var bottomDialog = this.doc.createElement("div");
      bottomDialog.className = "bottomDialogContent";
      var dialogButtonSet1 = this.doc.createElement("div");
      dialogButtonSet1.className = "dialogButtonEntry";
      //==========create tombol OK Cancel Print dan Export==================
      //create dulu container untuk button OK Cancelnya
      dialogButtonSet1.classList.add('dialogButtonOKCancel');
      //Create tombol OK Cancel
      var btnOK = this.doc.createElement("a");
      btnOK.className = "button";
      btnOK.nodeValue = "OK";
      btnOK.textContent = "OK";
      var inDisabledOK = args["btnOK"] === 'undefined' ? true : args["btnOK"];
      btnOK.style.width = "80px";
      btnOK.disabled = inDisabledOK.valueOf();
      //btnOK.disabled = true;
      var btnCancel = this.doc.createElement("a");
      btnCancel.className = "button";
      btnCancel.nodeValue = "Cancel";
      btnCancel.textContent = "Cancel";
      btnCancel.style.width = "80px";
      var inDisabledCancel = args["btnCancel"] === 'undefined' ? true : args["btnCancel"];
      btnCancel.disabled = inDisabledCancel.valueOf();
      dialogButtonSet1.appendChild(btnOK);
      dialogButtonSet1.appendChild(btnCancel);
      var dialogButtonSet2 = this.doc.createElement("div");
      dialogButtonSet2.className = "dialogButtonEntry";
      dialogButtonSet2.classList.add("dialogButtonRightOther");
      //create tombol Print dan Export
      var btnPrint = this.doc.createElement("a");
      //btnPrint.className = "btn-link";
      btnPrint.nodeValue = "Print Preview";
      btnPrint.textContent = "Print Preview";
      btnPrint.style.width = "120px";
      var inDisabledPrint = args["btnPrintPreview"] === 'undefined' ? true : args["btnPrintPreview"];
      if (inDisabledPrint.valueOf()) {
        btnPrint.style.cursor = "pointer"; // .cssText = "cursor:not-allowed;pointer - events: none;"
        btnPrint.style.removeProperty('pointerEvents')
      }
      btnPrint.style.marginRight = "0";
      btnPrint.style.paddingRight = "0";
      var btnExport = this.doc.createElement("a");
      btnExport.className = "btn-link";
      btnExport.nodeValue = "Export";
      btnExport.textContent = "Export"
      btnExport.style.width = "100px";
      var inDisabledExport = args["btnExport"] === 'undefined' ? true : args["btnExport"];
      if (inDisabledExport.valueOf()) {
        btnExport.style.cursor = "pointer"; // .cssText = "cursor:not-allowed;pointer - events: none;"
        btnExport.style.removeProperty('pointerEvents')
      }
      btnExport.style.marginRight = "0";
      btnExport.style.paddingRight = "0";
      dialogButtonSet2.appendChild(btnPrint);
      dialogButtonSet2.appendChild(btnExport);
      bottomDialog.appendChild(dialogButtonSet1);
      bottomDialog.appendChild(dialogButtonSet2); //3
      dialog.appendChild(headerDialog);
      dialog.appendChild(mainContentDialog);
      dialog.appendChild(bottomDialog);
      //  var scrollingPosition = this.getScrollingPosition();
      body.appendChild(dialog);
      //dialog.style.left = scrollingPosition[0] + parseInt(viewportSize[0] / 2) - parseInt(dialog.offsetWidth / 2) + "px";
      //dialog.style.top = scrollingPosition[1] + parseInt(viewportSize[1] / 2) - parseInt(dialog.offsetHeight/2) + "px";
      dialog.style.visibility = 'visible';
      //trigger showDialogEntry
      window.showDialogEntry(event);
      if (window.showOtherDialog) {
        window.showOtherDialog(event);
      }
      //============ set dialog to center ================
      dialog.style.top = '50%';
      dialog.style.left = '50%';
      dialog.style.setProperty('-ms-transform', 'translate(-50%, -50%)', 'important');
      dialog.style.setProperty('-webkit-transform', 'translate(-50%, -50%)', 'important');
      dialog.style.setProperty('-moz-transform', 'translate(-50%, -50%)', 'important');
      dialog.style.setProperty('transform', 'translate(-50%, -50%)', 'important');
      dialog.style.maxHeight = '614px';
      dialog.style.overflowX = "auto";
      //===============Enabled kan Dragdrop=================================
      NA.common.dialog.DragDrop.enable();
    } catch (error) {
      this.closeDialog(dialog);
      var mnuContainer = doc.querySelector('nav.navbar.navbar-default')
      if (mnuContainer) {
        mnuContainer.style.zIndex = "1000";
      }
      return true;
    }
    dialog.style.visibility = 'visible';
    return false;
  },
  closeDialog: function (dialog) {
    var dropSheet = NA.common.getElementID("dropSheet");
    if (dropSheet) {
      dropSheet.parentNode.removeChild(dropSheet);
      //remove attribute container dialog
      NA.common.dialog.DragDrop.disable();
      if (dialog) {
        dialog.parentNode.removeChild(dialog);
      }
    }
    var mnuContainer = this.doc.querySelector('nav.navbar.navbar-default')
    if (mnuContainer) {
      mnuContainer.style.zIndex = "1000";
    }
    return false;
  },
  //parameters
  //Entrycontnr = menu add edit delete ---> NA.common.dialog.doc.querySelector('ul.nav.navbar-nav')
  //titleHeader = Header dialog title
  //elementMenus = array component yang akan di pakai untuk click menu di side bar
  // SideMenuContainerClick = custom event handler yang akan mengeksekusi bila click event dalam array menu di click, default tidak usah di isi saja
  initDialog: function (Entrycontnr, titleHead, elementMenus, SideMenuContainerClick) {
    // init dialog untuk Open,  Edit,  Save,  Delete,  Export,  Print,  Help
    (function (elem, currentObj, titleHead, elements, otherHandler) {
      var settingsEditAdd = {
        btnOK: true,
        btnCancel: true,
        btnPrintPreview: true,
        btnExport: false,
        dialogTitle: titleHead
      },
        settingsOpen = {
          btnOK: false,
          btnCancel: false,
          btnPrintPreview: false,
          btnExport: false,
          dialogTitle: titleHead
        };
      settingsOther = {
        btnOK: true,
        btnCancel: true,
        btnPrintPreview: false,
        btnExport: true,
        dialogTitle: titleHead
      };
      //menu atas
      var ClickHandlerElem = function (event) {
        NA.NAEvent.preventDefault(event);
        var target = NA.NAEvent.getTarget(event);
        switch (target.innerText) {
          case ' Add': {
            if (!target.getAttribute('disabled')) {
              currentObj.createDialog(event, settingsEditAdd);
              window.status = "Add"
            }
            break;
          }
          case ' Open': {
            currentObj.createDialog(event, settingsOpen);
            window.status = "Open"
            break;
          }
          case ' Edit': {
            currentObj.createDialog(event, settingsEditAdd);
            window.status = "Edit"
            break;
          }
          default: {
            window.status = "";
            break;
          }
        }
      };
      if (elem) {
        NA.NAEvent.addHandler(elem, 'click', ClickHandlerElem);
      }
      //menu side
      var ClickHandlerElementMenu = function (event) {
        NA.NAEvent.preventDefault(event);
        currentObj.createDialog(event, settingsOther);
        window.status = "";
      };
      if (elements) {
        Array.prototype.forEach.call(elements, function (item) { //buat jadi foreach mesti convert dulu ke array
          if (SideMenuContainerClick && item) {
            if (!item.getAttribute('disabled')) {
              NA.NAEvent.addHandler(item, 'click', SideMenuContainerClick);
            }
          } else {
            if (item && (!item.getAttribute('disabled'))) {
              NA.NAEvent.addHandler(item, 'click', ClickHandlerElementMenu);
            }
          }
        });
      }
    })(Entrycontnr, this, titleHead, elementMenus, SideMenuContainerClick);
  }, // Save,  Delete,  Export,  Print,  Help
  //=================================Enabbled DragDrop Dialog==============================================================================
  DragDrop: function () {
    var dragging = null;

    function handleEvent(event) {
      //get event and target
      event = NA.NAEvent.getEvent(event);
      var target = NA.NAEvent.getTarget(event);
      //determine the type of event
      switch (event.type) {
        case "mousedown":
          if (target.className.indexOf("draggable") > -1) {
            dragging = target;
          }
          break;
        case "mousemove":
          if (dragging !== null) {
            var dialog = document.querySelector('div.containerDialog')
            //assign location
            dialog.style.left = event.clientX + "px";
            dialog.style.top = event.clientY + "px";
            dialog.style.transform = ''
          }
          break;
        case "mouseup":
          dragging = null;
          break;
      }
    };
    //public interface
    return {
      enable: function () {
        //var dialog = NA.common.dialog.doc.querySelector("div.containerDialog");
        NA.NAEvent.addHandler(window.document, "mousedown", handleEvent);
        NA.NAEvent.addHandler(window.document, "mousemove", handleEvent);
        NA.NAEvent.addHandler(window.document, "mouseup", handleEvent);
      },
      disable: function () {
        NA.NAEvent.removeHandler(window.document, "mousedown", handleEvent);
        NA.NAEvent.removeHandler(window.document, "mousemove", handleEvent);
        NA.NAEvent.removeHandler(window.document, "mouseup", handleEvent);
      }
    }
  }(),
};
NA.common.message = {
  _confirmDelete: 'Are you sure you want to delete data ?!!.\nOperation can not be undone',
  _canNotDelete: 'Can not delete data\nData has child-referenced',
  _canNotEdit: 'Can not edit data\nData may has child-referenced',
  _clearData: 'Are you sure you want to clear datas/reset ?!!.\nOperation can not be undone',
  _savingSucces: 'Data saved succesfuly.',
  _dataHasChanged: 'Data has changed, \nSave data before closing form ?',
  _refreshData: 'Data has changed \nIf you continue refreshing page\nAll Changes will be discarded\nContinue refreshing anyway ?.',
  _existsData: 'Data has existed',
  _titleInfo: 'Information',
  _confirmInfo: 'Confirmation',
  _titleError: 'Unhandled system exception due to the following error',
  _dataHasLost: 'Data has Lost',
  _canNotFindData: 'Can not find such data',
  _unsupportedCriteria: 'Operator is not supported for this kind of data\nPlease change criteria or column name',
  _canNotAddOtherPermsForGuest: 'This user is Guest, cannot add other permission except Allow View \n \n Hint : Change user\'s role if you want to add other permission',
  _unAuthorized: 'Un Authorized\nYou have been logged out.\nPlease login again !'
};
//mang misalkan user1 teh aya di posisi kieu, user1 keur nga update data .. ehh ai pek teh data eta karek bieu dihapus ku user2 ... terus nga handle na bere pesan(message) bahwa data eta teh geus dihapus ku user lain terus bere keterangan waktu jeng user anu ngahapus na ???
Object.defineProperties(NA.common.message, {
  confirmDelete: {
    get: function () {
      return this._confirmDelete;
    }
  },
  canNotDelete: {
    get: function () {
      return this._canNotDelete;
    }
  },
  canNotEdit: {
    get: function () {
      return this._canNotEdit;
    }
  },
  canNotFindData: {
    get: function () {
      return this._canNotFindData;
    }
  },
  clearData: {
    get: function () {
      return this._clearData;
    }
  },
  savingSucces: {
    get: function () {
      return this._savingSucces;
    }
  },
  dataHasChanged: {
    get: function () {
      return this._dataHasChanged;
    }
  },
  refreshData: {
    get: function () {
      return this._refreshData;
    }
  },
  existsData: {
    get: function () {
      return this._existsData;
    }
  },
  titleInfo: {
    get: function () {
      return this._titleInfo;
    }
  },
  titleError: {
    get: function () {
      return this._titleError;
    }
  },
  confirmInfo: {
    get: function () {
      return this._confirmInfo;
    }
  },
  dataHasLost: {
    get: function () {
      return this._dataHasLost;
    }
  },
  unsupportedCriteria: {
    get: function () {
      return this._unsupportedCriteria;
    }
  },
  canNotAddOtherPermsForGuest: {
    get: function () {
      return this._canNotAddOtherPermsForGuest;
    }
  },
  unAuthorized: {
    get: function () {
      return this._unAuthorized
    }
  }
});
NA.common.message.server = function (message) {
  var result;
  switch (message) {
    case '__hasref_edit':
      result = NA.common.message.canNotEdit;
      break;
    case '__hasref_del':
      result = NA.common.message.canNotDelete;
      break;
    case '__lost':
      result = NA.common.message.dataHasLost;
      break;
    case '__cannot_add_other_permission_guest':
      result = NA.common.message.canNotAddOtherPermsForGuest;
      break;
    default:
      result = message;
      break;
  }
  return result;
}
//=========================AJAX NAJS,(sudah test) =============================================
NA.common.AJAX = {
  XHR: {},
  Xsettings: {
    data: {},
    dataType: 'application/json', //content yang di kirim ke server jika post default nya application/json
    url: '',
    MIMEType: 'text/html', //method overrides the MIME type returned by the server,default 'text/html',override responsetype
    timeOut: 2000000
  },
};
NA.common.AJAX.createXHR = function () {
  if (typeof XMLHttpRequest != "undefined") {
    this.XHR = new XMLHttpRequest();
  } else if (typeof ActiveXObject != "undefined") {
    if (typeof arguments.callee.activeXString != "string") {
      var versions = ["MSXML2.XMLHttp.6.0", "MSXML2.XMLHttp.3.0",
        "MSXML2.XMLHttp"],
        i, len;
      for (i = 0, len = versions.length; i < len; i++) {
        try {
          var xhr = new ActiveXObject(versions[i]);
          arguments.callee.activeXString = versions[i];
          return xhr;
        } catch (ex) {
          //skip
        }
      }
    }
    this.XHR = new ActiveXObject(arguments.callee.activeXString);
  } else {
    throw new Error("No XHR object available.");
  }
  return this.XHR;
};
Object.defineProperty(NA.common.AJAX, 'settings', {
  get: function () {
    return this.Xsettings || {}
  },
  set: function (newSettings) {
    this.Xsettings = newSettings;
  }
});
NA.common.AJAX.POST = function (url, data, dataType, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
  if (NA.common.isObjectEmpty(this.XHR)) {
    this.createXHR();
  }
  var Xurl = url || this.settings.url;
  if (!Xurl || Xurl === '') {
    throw new Error("Please define URL");
  }
  var XData = data || this.settings.data,
    XdataType = dataType || this.settings.dataType;
  if (OnAJAXStart) {
    OnAJAXStart.call(this.XHR);
  }
  this.XHR.overrideMimeType(MIMEType || this.settings.MIMEType);
  if (OnLoad) {
    this.XHR.onload = OnLoad;
  }
  if (OnProgress) {
    this.XHR.onprogress = OnProgress;
  }
  if (OnError) {
    if (this.XHR.status == 401) {
      return NA.common.dialog.dialogAlert(NA.common.message.unAuthorized, NA.common.message.titleInfo, function () {
        window.location.href = NA.client.url.login_next
      })
    }
    this.XHR.onerror = OnError;
  }
  if (OnLoadEnd) {
    this.XHR.onloadend = OnLoadEnd;
  }
  this.XHR.open('POST', Xurl, true);
  if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {} && customRequestHeader != null) {
    this.XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value);
  }
  this.XHR.setRequestHeader('Content-Type', XdataType);
  //==========prevent browser catching============================
  this.XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
  this.XHR.setRequestHeader('Pragma', 'no - cache');
  this.XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
  this.XHR.setRequestHeader('X-CSRFToken', NA.CookieUtil.get('csrftoken'));
  this.XHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  //==============================================================
  //XHR.setRequestHeader('Accept :' + XdataType);
  if (OnBeforeSend) {
    OnBeforeSend.call(this.XHR);
  }
  if (XData) {
    this.XHR.send(XData);
  }
  return true;
};
NA.common.AJAX.GET = function (url, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
  if (NA.common.isObjectEmpty(this.XHR)) {
    this.createXHR();
  }
  var Xurl = url || this.settings.url;
  if (!Xurl || Xurl === '') {
    throw new Error("Please define URL");
  }
  if (OnAJAXStart) {
    OnAJAXStart.call(this.XHR);
  }
  this.XHR.overrideMimeType(MIMEType || this.settings.MIMEType);
  if (OnLoad) {
    this.XHR.onload = OnLoad;
  }
  this.XHR.open('GET', Xurl, true);
  if (OnProgress) {
    this.XHR.onprogress = OnProgress;
  }
  if (OnError) {
    if (this.XHR.status == 401) {
      return NA.common.dialog.dialogAlert(NA.common.message.unAuthorized, NA.common.message.titleInfo, function () {
        window.location.href = NA.client.url.login_next
      })
    }
    this.XHR.onerror = OnError;
  }
  if (OnLoadEnd) {
    this.XHR.onloadend = OnLoadEnd;
  }
  if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {} && customRequestHeader != null) {
    this.XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value);
  }
  //this.XHR.setRequestHeader('Content-Type', XdataType);
  //==========prevent browser catching============================
  this.XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
  this.XHR.setRequestHeader('Pragma', 'no - cache');
  this.XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
  //======= To determine if request is ajax =======
  this.XHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  //==============================================================
  if (OnBeforeSend) {
    OnBeforeSend.call(this.XHR);
  }
  this.XHR.send(null);
  return true;
};
NA.common.AJAX.SubmitForm = function (url, FormElement, MIMEType, OnAJAXStart, OnBeforeSend, OnLoad, OnProgress, OnError, OnLoadEnd, customRequestHeader) {
  if (NA.common.isObjectEmpty(this.XHR)) {
    this.createXHR();
  }
  var Xurl = url || this.settings.url;
  if (!Xurl || Xurl === '') {
    throw new Error("Please define URL");
  }
  //var XData = data || this.settings.data, XdataType = dataType || this.settings.dataType;
  if (OnAJAXStart) {
    OnAJAXStart.call(this.XHR);
  }
  this.XHR.overrideMimeType(MIMEType || this.settings.MIMEType);
  if (OnLoad) {
    this.XHR.onload = OnLoad;
  }
  this.XHR.open('POST', Xurl, true);
  if (OnLoadEnd) {
    this.XHR.onloadend = OnLoadEnd;
  }
  if (OnProgress) {
    this.XHR.onprogress = OnProgress;
  }
  if (OnError) {
    this.XHR.onerror = OnError;
  }
  if (typeof customRequestHeader != 'undefined' && customRequestHeader !== '' && customRequestHeader != {} && customRequestHeader != null) {
    this.XHR.setRequestHeader(customRequestHeader.key, customRequestHeader.value);
  }
  this.XHR.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  //==========prevent browser catching============================
  this.XHR.setRequestHeader('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0');
  this.XHR.setRequestHeader('Pragma', 'no - cache');
  this.XHR.setRequestHeader('Expires', 'Thu, 19 Nov 1981 08:52:00 GMT');
  //======= To determine if request is ajax =======
  this.XHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  //==============================================================
  this.XHR.send(NA.common.serializeForm(FormElement));
  return true;
};
NA.Privilege = {
  _roleName: 'SysAdmin',
  _rolCode: 'SA',
  _email: 'Nandar@yahoo.com',
  _password: '',
  _isAdmin: true,
  _permissions: {
    _allow_view: false,
    _allow_add: false,
    _allow_edit: false,
    _allow_delete: false
  }
}
Object.defineProperties(NA.Privilege, {
  RoleName: {
    get: function () {
      return this._roleName;
    },
    set: function (newValue) {
      return this._roleName = newValue;
    }
  },
  RolCode: {
    get: function () {
      return this._rolCode;
    },
    set: function (newValue) {
      this._rolCode = newValue;
    },
  },
  Email: {
    get: function () {
      return this._email;
    },
    set: function (newValue) {
      this._email = newValue;
    },
  },
  password: {
    get: function () {
      return this._password;
    },
    set: function (newValue) {
      this._password = newValue;
    },
  },
  IsAdmin: {
    get: function () {
      return this._isAdmin;
    },
    set: function (newValue) {
      this._isAdmin = newValue;
    },
  },
  Permissions: {
    get: function () {
      return this._permissions
    }
  }
});
Object.defineProperties(NA.Privilege.Permissions, {
  Allow_View: {
    get: function () {
      return this._allow_view;
    },
    set: function (newValue) {
      this._allow_view = newValue;
    }
  },
  Allow_Add: {
    get: function () {
      return this._allow_add;
    },
    set: function (newValue) {
      this._allow_add = newValue;
    }
  },
  Allow_Edit: {
    get: function () {
      return this._allow_edit;
    },
    set: function (newValue) {
      this._allow_edit = newValue;
    }
  },
  Allow_Delete: {
    get: function () {
      return this._allow_delete;
    },
    set: function (newValue) {
      this._allow_delete = newValue;
    }
  }
})
NA.Privilege.get_server_permissions = function (kwargs) {
  var form = kwargs['form_name'],
    email = kwargs['email'],
    success = kwargs['success'],
    done = kwargs['done'];
  var NAAjax = NA.common.AJAX;
  var url = '/MasterData/Privilege/permission/' + email + '/get_permission/?form_name=' + form;
  NAAjax.GET(url, 'application/json', null, null, function () {
    if (this.status == 200) {
      var response = JSON.parse(this.responseText)['message']
      success(response);
    };
  }, null, null, function () {
    done();
  });
};
NA.Privilege.read_privilege = function (form_name) {
  return NA.Privilege.get_server_permissions({
    form_name: form_name,
    email: NA.Privilege.Email, // this is has declared in layout.html
    success: function (permission) {
      for (var i = 0; i < permission.length; i++) {
        if (permission[i]['permission'] == 'Allow View') {
          NA.Privilege.Permissions.Allow_View = true;
        } else if (permission[i]['permission'] == 'Allow Add') {
          NA.Privilege.Permissions.Allow_Add = true;
        } else if (permission[i]['permission'] == 'Allow Edit') {
          NA.Privilege.Permissions.Allow_Edit = true;
        } else if (permission[i]['permission'] == 'Allow Delete') {
          NA.Privilege.Permissions.Allow_Delete = true;
        }
      }
    },
    done: function () {
      Object.freeze(NA.Privilege);
      var qs = qs || NA.common.qs
      var btn_add = qs('button#addData'),
        btn_edit = qs('button#editData'),
        btn_delete = qs('button#delData');
        btn_add.classList.remove('disabled');
        btn_delete.classList.remove('disabled');
        btn_edit.classList.remove('disabled');
      if (!NA.Privilege.Permissions.Allow_Add) {
        btn_add.setAttribute('class', 'active disabled');
        NA.NAEvent.addHandler(btn_add, 'click', function (event) {
          NA.NAEvent.preventDefault(event);
          NA.NAEvent.stopPropagation(event);
          event.stopImmediatePropagation();
          return false;
        });
        btn_add.style.cursor = 'not-allowed';
      };
      if (!NA.Privilege.Permissions.Allow_Edit) {
        btn_edit.setAttribute('class','active disabled');
        NA.NAEvent.addHandler(btn_edit, 'click', function (event) {
          NA.NAEvent.preventDefault(event);
          NA.NAEvent.stopPropagation(event);
          event.stopImmediatePropagation();
          return false;
        });
        btn_edit.style.cursor = 'not-allowed';
      };
      if (!NA.Privilege.Permissions.Allow_Delete) {
        btn_delete.setAttribute('class','active disabled');
        NA.NAEvent.addHandler(btn_delete, 'click', function (event) {
          NA.NAEvent.preventDefault(event);
          NA.NAEvent.stopPropagation(event);
          event.stopImmediatePropagation();
          return false;
        });
        btn_delete.style.cursor = 'not-allowed';
      }
    }
  });
}
//=================================================================

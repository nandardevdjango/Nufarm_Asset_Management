/* 
 * jqGrid  5.2.1
 * Copyright (c) 2008, Tony Tomov, tony@trirand.com  
 *
 * Modules: grid.base.js; jquery.fmatter.js; grid.common.js; grid.formedit.js; grid.filter.js; grid.inlinedit.js; grid.celledit.js; jqModal.js; jqDnR.js; grid.subgrid.js; grid.grouping.js; grid.treegrid.js; grid.pivot.js; grid.import.js; grid.export.js; grid.utils.js; grid.jqueryui.js; jquery.sortable.js;
 */! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery"], a) : a(jQuery)
}(function ($) {
    "use strict";
    $.jgrid = $.jgrid || {}, $.jgrid.hasOwnProperty("defaults") || ($.jgrid.defaults = {}), $.extend($.jgrid, {
        version: "5.2.1",
        htmlDecode: function (a) {
            return a && ("&nbsp;" === a || "&#160;" === a || 1 === a.length && 160 === a.charCodeAt(0)) ? "" : a ? String(a).replace(/&gt;/g, ">").replace(/&lt;/g, "<").replace(/&quot;/g, '"').replace(/&amp;/g, "&") : a
        },
        htmlEncode: function (a) {
            return a ? String(a).replace(/&/g, "&amp;").replace(/\"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;") : a
        },
        template: function (a) {
            var
            b, c = $.makeArray(arguments).slice(1),
                d = c.length;
            return null == a && (a = ""), a.replace(/\{([\w\-]+)(?:\:([\w\.]*)(?:\((.*?)?\))?)?\}/g, function (a, e) {
                if (!isNaN(parseInt(e, 10))) return c[parseInt(e, 10)];
                for (b = 0; b < d; b++) if ($.isArray(c[b])) for (var
                f = c[b], g = f.length; g--;) if (e === f[g].nm) return f[g].v
            })
        },
        msie: function () {
            return $.jgrid.msiever() > 0
        },
        msiever: function () {
            var
            a = 0,
                b = window.navigator.userAgent,
                c = b.indexOf("MSIE");
            return c > 0 ? a = parseInt(b.substring(c + 5, b.indexOf(".", c))) : navigator.userAgent.match(/Trident\/7\./) && (a = 11), a
        },
        getCellIndex: function (a) {
            var
            b = $(a);
            return b.is("tr") ? -1 : (b = (b.is("td") || b.is("th") ? b : b.closest("td,th"))[0], $.jgrid.msie() ? $.inArray(b, b.parentNode.cells) : b.cellIndex)
        },
        stripHtml: function (a) {
            a = String(a);
            var
            b = /<("[^"]*"|'[^']*'|[^'">])*>/gi;
            return a ? (a = a.replace(b, ""), a && "&nbsp;" !== a && "&#160;" !== a ? a.replace(/\"/g, "'") : "") : a
        },
        stripPref: function (a, b) {
            var
            c = $.type(a);
            return "string" !== c && "number" !== c || (a = String(a), b = "" !== a ? String(b).replace(String(a), "") : b), b
        },
        useJSON: !0,
        parse: function (jsonString) {
            var
            js = jsonString;
            return "while(1);" === js.substr(0, 9) && (js = js.substr(9)), "/*" === js.substr(0, 2) && (js = js.substr(2, js.length - 4)), js || (js = "{}"), !0 === $.jgrid.useJSON && "object" == typeof
            JSON && "function" == typeof
            JSON.parse ? JSON.parse(js) : eval("(" + js + ")")
        },
        parseDate: function (a, b, c, d) {
            var
            e, f, g, h = /\\.|[dDjlNSwzWFmMntLoYyaABgGhHisueIOPTZcrU]/g,
                i = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
                j = /[^-+\dA-Z]/g,
                k = new
                RegExp("^/Date\\((([-+])?[0-9]+)(([-+])([0-9]{2})([0-9]{2}))?\\)/$"),
                l = "string" == typeof
                b ? b.match(k) : null,
                m = function (a, b) {
                    for (a = String(a), b = parseInt(b, 10) || 2; a.length < b;) a = "0" + a;
                    return a
                }, n = {
                    m: 1,
                    d: 1,
                    y: 1970,
                    h: 0,
                    i: 0,
                    s: 0,
                    u: 0
                }, o = 0,
                p = function (a, b) {
                    return 0 === a ? 12 === b && (b = 0) : 12 !== b && (b += 12), b
                }, q = 0;
            if (void
            0 === d && (d = $.jgrid.getRegional(this, "formatter.date")), void
            0 === d.parseRe && (d.parseRe = /[#%\\\/:_;.,\t\s-]/), d.masks.hasOwnProperty(a) && (a = d.masks[a]), b && null != b) if (isNaN(b - 0) || "u" !== String(a).toLowerCase()) if (b.constructor === Date) o = b;
            else if (null !== l) o = new
            Date(parseInt(l[1], 10)), l[3] && (q = 60 * Number(l[5]) + Number(l[6]), q *= "-" === l[4] ? 1 : -1, q -= o.getTimezoneOffset(), o.setTime(Number(Number(o) + 60 * q * 1e3)));
            else {
                for ("ISO8601Long" === d.srcformat && "Z" === b.charAt(b.length - 1) && (q -= (new
                Date).getTimezoneOffset()), b = String(b).replace(/\T/g, "#").replace(/\t/, "%").split(d.parseRe), a = a.replace(/\T/g, "#").replace(/\t/, "%").split(d.parseRe), f = 0, g = a.length; f < g; f++) {
                    switch (a[f]) {
                        case "M":
                            e = $.inArray(b[f], d.monthNames), -1 !== e && e < 12 && (b[f] = e + 1, n.m = b[f]);
                            break;
                        case "F":
                            e = $.inArray(b[f], d.monthNames, 12), -1 !== e && e > 11 && (b[f] = e + 1 - 12, n.m = b[f]);
                            break;
                        case "n":
                            a[f] = "m";
                            break;
                        case "j":
                            a[f] = "d";
                            break;
                        case "a":
                            e = $.inArray(b[f], d.AmPm), -1 !== e && e < 2 && b[f] === d.AmPm[e] && (b[f] = e, n.h = p(b[f], n.h));
                            break;
                        case "A":
                            e = $.inArray(b[f], d.AmPm), -1 !== e && e > 1 && b[f] === d.AmPm[e] && (b[f] = e - 2, n.h = p(b[f], n.h));
                            break;
                        case "g":
                            n.h = parseInt(b[f], 10)
                    }
                    void
                    0 !== b[f] && (n[a[f].toLowerCase()] = parseInt(b[f], 10))
                }
                if (n.f && (n.m = n.f), 0 === n.m && 0 === n.y && 0 === n.d) return "&#160;";
                n.m = parseInt(n.m, 10) - 1;
                var
                r = n.y;
                r >= 70 && r <= 99 ? n.y = 1900 + n.y : r >= 0 && r <= 69 && (n.y = 2e3 + n.y), o = new
                Date(n.y, n.m, n.d, n.h, n.i, n.s, n.u), 0 !== q && o.setTime(Number(Number(o) + 60 * q * 1e3))
            } else o = new
            Date(1e3 * parseFloat(b));
            else o = new
            Date(n.y, n.m, n.d, n.h, n.i, n.s, n.u);
            if (d.userLocalTime && 0 === q && 0 !== (q -= (new
            Date).getTimezoneOffset()) && o.setTime(Number(Number(o) + 60 * q * 1e3)), void
            0 === c) return o;
            d.masks.hasOwnProperty(c) ? c = d.masks[c] : c || (c = "Y-m-d");
            var
            s = o.getHours(),
                t = o.getMinutes(),
                u = o.getDate(),
                v = o.getMonth() + 1,
                w = o.getTimezoneOffset(),
                x = o.getSeconds(),
                y = o.getMilliseconds(),
                z = o.getDay(),
                A = o.getFullYear(),
                B = (z + 6) % 7 + 1,
                C = (new
                Date(A, v - 1, u) - new
                Date(A, 0, 1)) / 864e5,
                D = {
                    d: m(u),
                    D: d.dayNames[z],
                    j: u,
                    l: d.dayNames[z + 7],
                    N: B,
                    S: d.S(u),
                    w: z,
                    z: C,
                    W: B < 5 ? Math.floor((C + B - 1) / 7) + 1 : Math.floor((C + B - 1) / 7) || ((new
                    Date(A - 1, 0, 1).getDay() + 6) % 7 < 4 ? 53 : 52),
                    F: d.monthNames[v - 1 + 12],
                    m: m(v),
                    M: d.monthNames[v - 1],
                    n: v,
                    t: "?",
                    L: "?",
                    o: "?",
                    Y: A,
                    y: String(A).substring(2),
                    a: s < 12 ? d.AmPm[0] : d.AmPm[1],
                    A: s < 12 ? d.AmPm[2] : d.AmPm[3],
                    B: "?",
                    g: s % 12 || 12,
                    G: s,
                    h: m(s % 12 || 12),
                    H: m(s),
                    i: m(t),
                    s: m(x),
                    u: y,
                    e: "?",
                    I: "?",
                    O: (w > 0 ? "-" : "+") + m(100 * Math.floor(Math.abs(w) / 60) + Math.abs(w) % 60, 4),
                    P: "?",
                    T: (String(o).match(i) || [""]).pop().replace(j, ""),
                    Z: "?",
                    c: "?",
                    r: "?",
                    U: Math.floor(o / 1e3)
                };
            return c.replace(h, function (a) {
                return D.hasOwnProperty(a) ? D[a] : a.substring(1)
            })
        },
        jqID: function (a) {
            return String(a).replace(/[!"#$%&'()*+,.\/:; <=>?@\[\\\]\^`{|}~]/g, "\\$&")
        },
        guid: 1,
        uidPref: "jqg",
        randId: function (a) {
            return (a || $.jgrid.uidPref) + $.jgrid.guid++
        },
        getAccessor: function (a, b) {
            var
            c, d, e, f = [];
            if ("function" == typeof
            b) return b(a);
            if (void
            0 === (c = a[b])) try {
                if ("string" == typeof
                b && (f = b.split(".")), e = f.length) for (c = a; c && e--;) d = f.shift(), c = c[d]
            } catch (a) {}
            return c
        },
        getXmlData: function (a, b, c) {
            var
            d, e = "string" == typeof
            b ? b.match(/^(.*)\[(\w+)\]$/) : null;
            return "function" == typeof
            b ? b(a) : e && e[2] ? e[1] ? $(e[1], a).attr(e[2]) : $(a).attr(e[2]) : (d = $(b, a), c ? d : d.length > 0 ? $(d).text() : void
            0)
        },
        cellWidth: function () {
            var
            a = $("<div class='ui-jqgrid' style='left:10000px'><table class='ui-jqgrid-btable ui-common-table' style='width:5px;'><tr class='jqgrow'><td style='width:5px;display:block;'></td></tr></table></div>"),
                b = a.appendTo("body").find("td").width();
            return a.remove(), Math.abs(b - 5) > .1
        },
        isLocalStorage: function () {
            try {
                return "localStorage" in window && null !== window.localStorage
            } catch (a) {
                return !1
            }
        },
        getRegional: function (a, b, c) {
            var
            d;
            return void
            0 !== c ? c : (a.p && a.p.regional && $.jgrid.regional && (d = $.jgrid.getAccessor($.jgrid.regional[a.p.regional] || {}, b)), void
            0 === d && (d = $.jgrid.getAccessor($.jgrid, b)), d)
        },
        isMobile: function () {
            try {
                return !!/Android|webOS|iPhone|iPad|iPod|pocket|psp|kindle|avantgo|blazer|midori|Tablet|Palm|maemo|plucker|phone|BlackBerry|symbian|IEMobile|mobile|ZuneWP7|Windows Phone|Opera Mini/i.test(navigator.userAgent)
            } catch (a) {
                return !1
            }
        },
        cell_width: !0,
        ajaxOptions: {},
        from: function (source) {
            var
            $t = this,
                QueryObject = function (d, q) {
                    "string" == typeof
                    d && (d = $.data(d));
                    var
                    self = this,
                        _data = d,
                        _usecase = !0,
                        _trim = !1,
                        _query = q,
                        _stripNum = /[\$,%]/g,
                        _lastCommand = null,
                        _lastField = null,
                        _orDepth = 0,
                        _negate = !1,
                        _queuedOperator = "",
                        _sorting = [],
                        _useProperties = !0;
                    if ("object" != typeof
                    d || !d.push) throw "data provides is not an array";
                    return d.length > 0 && (_useProperties = "object" == typeof
                    d[0]), this._hasData = function () {
                        return null !== _data && 0 !== _data.length
                    }, this._getStr = function (a) {
                        var
                        b = [];
                        return _trim && b.push("jQuery.trim("), b.push("String(" + a + ")"), _trim && b.push(")"), _usecase || b.push(".toLowerCase()"), b.join("")
                    }, this._strComp = function (a) {
                        return "string" == typeof
                        a ? ".toString()" : ""
                    }, this._group = function (a, b) {
                        return {
                            field: a.toString(),
                            unique: b,
                            items: []
                        }
                    }, this._toStr = function (a) {
                        return _trim && (a = $.trim(a)), a = a.toString().replace(/\\/g, "\\\\").replace(/\"/g, '\\"'), _usecase ? a : a.toLowerCase()
                    }, this._funcLoop = function (a) {
                        var
                        b = [];
                        return $.each(_data, function (c, d) {
                            b.push(a(d))
                        }), b
                    }, this._append = function (a) {
                        var
                        b;
                        for (null === _query ? _query = "" : _query += "" === _queuedOperator ? " && " : _queuedOperator, b = 0; b < _orDepth; b++) _query += "(";
                        _negate && (_query += "!"), _query += "(" + a + ")", _negate = !1, _queuedOperator = "", _orDepth = 0
                    }, this._setCommand = function (a, b) {
                        _lastCommand = a, _lastField = b
                    }, this._resetNegate = function () {
                        _negate = !1
                    }, this._repeatCommand = function (a, b) {
                        return null === _lastCommand ? self : null !== a && null !== b ? _lastCommand(a, b) : null === _lastField ? _lastCommand(a) : _useProperties ? _lastCommand(_lastField, a) : _lastCommand(a)
                    }, this._equals = function (a, b) {
                        return 0 === self._compare(a, b, 1)
                    }, this._compare = function (a, b, c) {
                        var
                        d = Object.prototype.toString;
                        return void
                        0 === c && (c = 1), void
                        0 === a && (a = null), void
                        0 === b && (b = null), null === a && null === b ? 0 : null === a && null !== b ? 1 : null !== a && null === b ? -1 : "[object Date]" === d.call(a) && "[object Date]" === d.call(b) ? a < b ? -c : a > b ? c : 0 : (_usecase || "number" == typeof
                        a || "number" == typeof
                        b || (a = String(a), b = String(b)), a < b ? -c : a > b ? c : 0)
                    }, this._performSort = function () {
                        0 !== _sorting.length && (_data = self._doSort(_data, 0))
                    }, this._doSort = function (a, b) {
                        var
                        c = _sorting[b].by,
                            d = _sorting[b].dir,
                            e = _sorting[b].type,
                            f = _sorting[b].datefmt,
                            g = _sorting[b].sfunc;
                        if (b === _sorting.length - 1) return self._getOrder(a, c, d, e, f, g);
                        b++;
                        var
                        h, i, j, k = self._getGroup(a, c, d, e, f),
                            l = [];
                        for (h = 0; h < k.length; h++) for (j = self._doSort(k[h].items, b), i = 0; i < j.length; i++) l.push(j[i]);
                        return l
                    }, this._getOrder = function (a, b, c, d, e, f) {
                        var
                        g, h, i, j, k = [],
                            l = [],
                            m = "a" === c ? 1 : -1;
                        void
                        0 === d && (d = "text"), j = "float" === d || "number" === d || "currency" === d || "numeric" === d ? function (a) {
                            var
                            b = parseFloat(String(a).replace(_stripNum, ""));
                            return isNaN(b) ? Number.NEGATIVE_INFINITY : b
                        } : "int" === d || "integer" === d ? function (a) {
                            return a ? parseFloat(String(a).replace(_stripNum, "")) : Number.NEGATIVE_INFINITY
                        } : "date" === d || "datetime" === d ? function (a) {
                            return $.jgrid.parseDate.call($t, e, a).getTime()
                        } : $.isFunction(d) ? d : function (a) {
                            return a = a ? $.trim(String(a)) : "", _usecase ? a : a.toLowerCase()
                        }, $.each(a, function (a, c) {
                            h = "" !== b ? $.jgrid.getAccessor(c, b) : c, void
                            0 === h && (h = ""), h = j(h, c), l.push({
                                vSort: h,
                                index: a
                            })
                        }), $.isFunction(f) ? l.sort(function (a, b) {
                            return f.call(this, a.vSort, b.vSort, m, a, b)
                        }) : l.sort(function (a, b) {
                            return self._compare(a.vSort, b.vSort, m)
                        }), i = 0;
                        for (var
                        n = a.length; i < n;) g = l[i].index, k.push(a[g]), i++;
                        return k
                    }, this._getGroup = function (a, b, c, d, e) {
                        var
                        f, g = [],
                            h = null,
                            i = null;
                        return $.each(self._getOrder(a, b, c, d, e), function (a, c) {
                            f = $.jgrid.getAccessor(c, b), null == f && (f = ""), self._equals(i, f) || (i = f, null !== h && g.push(h), h = self._group(b, f)), h.items.push(c)
                        }), null !== h && g.push(h), g
                    }, this.ignoreCase = function () {
                        return _usecase = !1, self
                    }, this.useCase = function () {
                        return _usecase = !0, self
                    }, this.trim = function () {
                        return _trim = !0, self
                    }, this.noTrim = function () {
                        return _trim = !1, self
                    }, this.execute = function () {
                        var
                        match = _query,
                            results = [];
                        return null === match ? self : ($.each(_data, function () {
                            eval(match) && results.push(this)
                        }), _data = results, self)
                    }, this.data = function () {
                        return _data
                    }, this.select = function (a) {
                        if (self._performSort(), !self._hasData()) return [];
                        if (self.execute(), $.isFunction(a)) {
                            var
                            b = [];
                            return $.each(_data, function (c, d) {
                                b.push(a(d))
                            }), b
                        }
                        return _data
                    }, this.hasMatch = function () {
                        return !!self._hasData() && (self.execute(), _data.length > 0)
                    }, this.andNot = function (a, b, c) {
                        return _negate = !_negate, self.and(a, b, c)
                    }, this.orNot = function (a, b, c) {
                        return _negate = !_negate, self.or(a, b, c)
                    }, this.not = function (a, b, c) {
                        return self.andNot(a, b, c)
                    }, this.and = function (a, b, c) {
                        return _queuedOperator = " && ", void
                        0 === a ? self : self._repeatCommand(a, b, c)
                    }, this.or = function (a, b, c) {
                        return _queuedOperator = " || ", void
                        0 === a ? self : self._repeatCommand(a, b, c)
                    }, this.orBegin = function () {
                        return _orDepth++, self
                    }, this.orEnd = function () {
                        return null !== _query && (_query += ")"), self
                    }, this.isNot = function (a) {
                        return _negate = !_negate, self.is(a)
                    }, this.is = function (a) {
                        return self._append("this." + a), self._resetNegate(), self
                    }, this._compareValues = function (a, b, c, d, e) {
                        var
                        f;
                        f = _useProperties ? "jQuery.jgrid.getAccessor(this,'" + b + "')" : "this", void
                        0 === c && (c = null);
                        var
                        g = c,
                            h = void
                            0 === e.stype ? "text" : e.stype;
                        if (null !== c) switch (h) {
                            case "int":
                            case "integer":
                                g = isNaN(Number(g)) || "" === g ? "0" : g, f = "parseInt(" + f + ",10)", g = "parseInt(" + g + ",10)";
                                break;
                            case "float":
                            case "number":
                            case "numeric":
                                g = String(g).replace(_stripNum, ""), g = isNaN(Number(g)) || "" === g ? "0" : g, f = "parseFloat(" + f + ")", g = "parseFloat(" + g + ")";
                                break;
                            case "date":
                            case "datetime":
                                g = String($.jgrid.parseDate.call($t, e.srcfmt || "Y-m-d", g).getTime()), f = 'jQuery.jgrid.parseDate.call(jQuery("#' + $.jgrid.jqID($t.p.id) + '")[0],"' + e.srcfmt + '",' + f + ").getTime()";
                                break;
                            default:
                                f = self._getStr(f), g = self._getStr('"' + self._toStr(g) + '"')
                        }
                        return self._append(f + " " + d + " " + g), self._setCommand(a, b), self._resetNegate(), self
                    }, this.equals = function (a, b, c) {
                        return self._compareValues(self.equals, a, b, "==", c)
                    }, this.notEquals = function (a, b, c) {
                        return self._compareValues(self.equals, a, b, "!==", c)
                    }, this.isNull = function (a, b, c) {
                        return self._compareValues(self.equals, a, null, "===", c)
                    }, this.greater = function (a, b, c) {
                        return self._compareValues(self.greater, a, b, ">", c)
                    }, this.less = function (a, b, c) {
                        return self._compareValues(self.less, a, b, "<", c)
                    }, this.greaterOrEquals = function (a, b, c) {
                        return self._compareValues(self.greaterOrEquals, a, b, ">=", c)
                    }, this.lessOrEquals = function (a, b, c) {
                        return self._compareValues(self.lessOrEquals, a, b, "<=", c)
                    }, this.startsWith = function (a, b) {
                        var
                        c = null == b ? a : b,
                            d = _trim ? $.trim(c.toString()).length : c.toString().length;
                        return _useProperties ? self._append(self._getStr("jQuery.jgrid.getAccessor(this,'" + a + "')") + ".substr(0," + d + ") == " + self._getStr('"' + self._toStr(b) + '"')) : (null != b && (d = _trim ? $.trim(b.toString()).length : b.toString().length), self._append(self._getStr("this") + ".substr(0," + d + ") == " + self._getStr('"' + self._toStr(a) + '"'))), self._setCommand(self.startsWith, a), self._resetNegate(), self
                    }, this.endsWith = function (a, b) {
                        var
                        c = null == b ? a : b,
                            d = _trim ? $.trim(c.toString()).length : c.toString().length;
                        return _useProperties ? self._append(self._getStr("jQuery.jgrid.getAccessor(this,'" + a + "')") + ".substr(" + self._getStr("jQuery.jgrid.getAccessor(this,'" + a + "')") + ".length-" + d + "," + d + ') == "' + self._toStr(b) + '"') : self._append(self._getStr("this") + ".substr(" + self._getStr("this") + '.length-"' + self._toStr(a) + '".length,"' + self._toStr(a) + '".length) == "' + self._toStr(a) + '"'), self._setCommand(self.endsWith, a), self._resetNegate(), self
                    }, this.contains = function (a, b) {
                        return _useProperties ? self._append(self._getStr("jQuery.jgrid.getAccessor(this,'" + a + "')") + '.indexOf("' + self._toStr(b) + '",0) > -1') : self._append(self._getStr("this") + '.indexOf("' + self._toStr(a) + '",0) > -1'), self._setCommand(self.contains, a), self._resetNegate(), self
                    }, this.groupBy = function (a, b, c, d) {
                        return self._hasData() ? self._getGroup(_data, a, b, c, d) : null
                    }, this.orderBy = function (a, b, c, d, e) {
                        return b = null == b ? "a" : $.trim(b.toString().toLowerCase()), null == c && (c = "text"), null == d && (d = "Y-m-d"), null == e && (e = !1), "desc" !== b && "descending" !== b || (b = "d"), "asc" !== b && "ascending" !== b || (b = "a"), _sorting.push({
                            by: a,
                            dir: b,
                            type: c,
                            datefmt: d,
                            sfunc: e
                        }), self
                    }, self
                };
            return new
            QueryObject(source, null)
        },
        getMethod: function (a) {
            return this.getAccessor($.fn.jqGrid, a)
        },
        extend: function (a) {
            $.extend($.fn.jqGrid, a), this.no_legacy_api || $.fn.extend(a)
        },
        clearBeforeUnload: function (a) {
            var
            b, c = $("#" + $.jgrid.jqID(a))[0];
            if (c.grid) {
                b = c.grid, $.isFunction(b.emptyRows) && b.emptyRows.call(c, !0, !0), $(document).off("mouseup.jqGrid" + c.p.id), $(b.hDiv).off("mousemove"), $(c).off();
                var
                d, e = b.headers.length,
                    f = ["formatCol", "sortData", "updatepager", "refreshIndex", "setHeadCheckBox", "constructTr", "formatter", "addXmlData", "addJSONData", "grid", "p", "addLocalData"];
                for (d = 0; d < e; d++) b.headers[d].el = null;
                for (d in b) b.hasOwnProperty(d) && (b[d] = null);
                for (d in c.p) c.p.hasOwnProperty(d) && (c.p[d] = $.isArray(c.p[d]) ? [] : null);
                for (e = f.length, d = 0; d < e; d++) c.hasOwnProperty(f[d]) && (c[f[d]] = null, delete
                c[f[d]])
            }
        },
        gridUnload: function (a) {
            if (a) {
                a = $.trim(a), 0 === a.indexOf("#") && (a = a.substring(1));
                var
                b = $("#" + $.jgrid.jqID(a))[0];
                if (b.grid) {
                    var
                    c = {
                        id: $(b).attr("id"),
                        cl: $(b).attr("class")
                    };
                    b.p.pager && $(b.p.pager).off().empty().removeClass("ui-state-default ui-jqgrid-pager ui-corner-bottom");
                    var
                    d = document.createElement("table");
                    d.className = c.cl;
                    var
                    e = $.jgrid.jqID(b.id);
                    $(d).removeClass("ui-jqgrid-btable ui-common-table").insertBefore("#gbox_" + e), 1 === $(b.p.pager).parents("#gbox_" + e).length && $(b.p.pager).insertBefore("#gbox_" + e), $.jgrid.clearBeforeUnload(a), $("#gbox_" + e).remove(), $(d).attr({
                        id: c.id
                    }), $("#alertmod_" + $.jgrid.jqID(a)).remove()
                }
            }
        },
        gridDestroy: function (a) {
            if (a) {
                a = $.trim(a), 0 === a.indexOf("#") && (a = a.substring(1));
                var
                b = $("#" + $.jgrid.jqID(a))[0];
                if (b.grid) {
                    b.p.pager && $(b.p.pager).remove();
                    try {
                        $.jgrid.clearBeforeUnload(a), $("#gbox_" + $.jgrid.jqID(a)).remove()
                    } catch (a) {}
                }
            }
        },
        styleUI: {
            jQueryUI: {
                common: {
                    disabled: "ui-state-disabled",
                    highlight: "ui-state-highlight",
                    hover: "ui-state-hover",
                    cornerall: "ui-corner-all",
                    cornertop: "ui-corner-top",
                    cornerbottom: "ui-corner-bottom",
                    hidden: "ui-helper-hidden",
                    icon_base: "ui-icon",
                    overlay: "ui-widget-overlay",
                    active: "ui-state-active",
                    error: "ui-state-error",
                    button: "ui-state-default ui-corner-all",
                    content: "ui-widget-content"
                },
                base: {
                    entrieBox: "ui-widget ui-widget-content ui-corner-all",
                    viewBox: "",
                    headerTable: "",
                    headerBox: "ui-state-default",
                    rowTable: "",
                    rowBox: "ui-widget-content",
                    stripedTable: "ui-jqgrid-table-striped",
                    footerTable: "",
                    footerBox: "ui-widget-content",
                    headerDiv: "ui-state-default",
                    gridtitleBox: "ui-widget-header ui-corner-top ui-helper-clearfix",
                    customtoolbarBox: "ui-state-default",
                    loadingBox: "ui-state-default ui-state-active",
                    rownumBox: "ui-state-default",
                    scrollBox: "ui-widget-content",
                    multiBox: "",
                    pagerBox: "ui-state-default ui-corner-bottom",
                    pagerTable: "",
                    toppagerBox: "ui-state-default",
                    pgInput: "ui-corner-all",
                    pgSelectBox: "ui-widget-content ui-corner-all",
                    pgButtonBox: "ui-corner-all",
                    icon_first: "ui-icon-seek-first",
                    icon_prev: "ui-icon-seek-prev",
                    icon_next: "ui-icon-seek-next",
                    icon_end: "ui-icon-seek-end",
                    icon_asc: "ui-icon-triangle-1-n",
                    icon_desc: "ui-icon-triangle-1-s",
                    icon_caption_open: "ui-icon-circle-triangle-n",
                    icon_caption_close: "ui-icon-circle-triangle-s"
                },
                modal: {
                    modal: "ui-widget ui-widget-content ui-corner-all ui-dialog",
                    header: "ui-widget-header ui-corner-all ui-helper-clearfix",
                    content: "ui-widget-content",
                    resizable: "ui-resizable-handle ui-resizable-se",
                    icon_close: "ui-icon-closethick",
                    icon_resizable: "ui-icon-gripsmall-diagonal-se"
                },
                celledit: {
                    inputClass: "ui-widget-content ui-corner-all"
                },
                inlinedit: {
                    inputClass: "ui-widget-content ui-corner-all",
                    icon_edit_nav: "ui-icon-pencil",
                    icon_add_nav: "ui-icon-plus",
                    icon_save_nav: "ui-icon-disk",
                    icon_cancel_nav: "ui-icon-cancel"
                },
                formedit: {
                    inputClass: "ui-widget-content ui-corner-all",
                    icon_prev: "ui-icon-triangle-1-w",
                    icon_next: "ui-icon-triangle-1-e",
                    icon_save: "ui-icon-disk",
                    icon_close: "ui-icon-close",
                    icon_del: "ui-icon-scissors",
                    icon_cancel: "ui-icon-cancel"
                },
                navigator: {
                    icon_edit_nav: "ui-icon-pencil",
                    icon_add_nav: "ui-icon-plus",
                    icon_del_nav: "ui-icon-trash",
                    icon_search_nav: "ui-icon-search",
                    icon_refresh_nav: "ui-icon-refresh",
                    icon_view_nav: "ui-icon-document",
                    icon_newbutton_nav: "ui-icon-newwin"
                },
                grouping: {
                    icon_plus: "ui-icon-circlesmall-plus",
                    icon_minus: "ui-icon-circlesmall-minus"
                },
                filter: {
                    table_widget: "ui-widget ui-widget-content",
                    srSelect: "ui-widget-content ui-corner-all",
                    srInput: "ui-widget-content ui-corner-all",
                    menu_widget: "ui-widget ui-widget-content ui-corner-all",
                    icon_search: "ui-icon-search",
                    icon_reset: "ui-icon-arrowreturnthick-1-w",
                    icon_query: "ui-icon-comment"
                },
                subgrid: {
                    icon_plus: "ui-icon-plus",
                    icon_minus: "ui-icon-minus",
                    icon_open: "ui-icon-carat-1-sw"
                },
                treegrid: {
                    icon_plus: "ui-icon-triangle-1-",
                    icon_minus: "ui-icon-triangle-1-s",
                    icon_leaf: "ui-icon-radio-off"
                },
                fmatter: {
                    icon_edit: "ui-icon-pencil",
                    icon_add: "ui-icon-plus",
                    icon_save: "ui-icon-disk",
                    icon_cancel: "ui-icon-cancel",
                    icon_del: "ui-icon-trash"
                },
                colmenu: {
                    menu_widget: "ui-widget ui-widget-content ui-corner-all",
                    input_checkbox: "ui-widget ui-widget-content",
                    filter_select: "ui-widget-content ui-corner-all",
                    filter_input: "ui-widget-content ui-corner-all",
                    icon_menu: "ui-icon-comment",
                    icon_sort_asc: "ui-icon-arrow-1-n",
                    icon_sort_desc: "ui-icon-arrow-1-s",
                    icon_columns: "ui-icon-extlink",
                    icon_filter: "ui-icon-calculator",
                    icon_group: "ui-icon-grip-solid-horizontal",
                    icon_freeze: "ui-icon-grip-solid-vertical",
                    icon_move: "ui-icon-arrow-4"
                }
            },
            Bootstrap: {
                common: {
                    disabled: "ui-disabled",
                    highlight: "success",
                    hover: "active",
                    cornerall: "",
                    cornertop: "",
                    cornerbottom: "",
                    hidden: "",
                    icon_base: "glyphicon",
                    overlay: "ui-overlay",
                    active: "active",
                    error: "bg-danger",
                    button: "btn btn-default",
                    content: ""
                },
                base: {
                    entrieBox: "",
                    viewBox: "table-responsive",
                    headerTable: "table table-bordered",
                    headerBox: "",
                    rowTable: "table table-bordered",
                    rowBox: "",
                    stripedTable: "table-striped",
                    footerTable: "table table-bordered",
                    footerBox: "",
                    headerDiv: "",
                    gridtitleBox: "",
                    customtoolbarBox: "",
                    loadingBox: "row",
                    rownumBox: "active",
                    scrollBox: "",
                    multiBox: "checkbox",
                    pagerBox: "",
                    pagerTable: "table",
                    toppagerBox: "",
                    pgInput: "form-control",
                    pgSelectBox: "form-control",
                    pgButtonBox: "",
                    icon_first: "glyphicon-step-backward",
                    icon_prev: "glyphicon-backward",
                    icon_next: "glyphicon-forward",
                    icon_end: "glyphicon-step-forward",
                    icon_asc: "glyphicon-triangle-top",
                    icon_desc: "glyphicon-triangle-bottom",
                    icon_caption_open: "glyphicon-circle-arrow-up",
                    icon_caption_close: "glyphicon-circle-arrow-down"
                },
                modal: {
                    modal: "modal-content",
                    header: "modal-header",
                    title: "modal-title",
                    content: "modal-body",
                    resizable: "ui-resizable-handle ui-resizable-se",
                    icon_close: "glyphicon-remove-circle",
                    icon_resizable: "glyphicon-import"
                },
                celledit: {
                    inputClass: "form-control"
                },
                inlinedit: {
                    inputClass: "form-control",
                    icon_edit_nav: "glyphicon-edit",
                    icon_add_nav: "glyphicon-plus",
                    icon_save_nav: "glyphicon-save",
                    icon_cancel_nav: "glyphicon-remove-circle"
                },
                formedit: {
                    inputClass: "form-control",
                    icon_prev: "glyphicon-step-backward",
                    icon_next: "glyphicon-step-forward",
                    icon_save: "glyphicon-save",
                    icon_close: "glyphicon-remove-circle",
                    icon_del: "glyphicon-trash",
                    icon_cancel: "glyphicon-remove-circle"
                },
                navigator: {
                    icon_edit_nav: "glyphicon-edit",
                    icon_add_nav: "glyphicon-plus",
                    icon_del_nav: "glyphicon-trash",
                    icon_search_nav: "glyphicon-search",
                    icon_refresh_nav: "glyphicon-refresh",
                    icon_view_nav: "glyphicon-info-sign",
                    icon_newbutton_nav: "glyphicon-new-window"
                },
                grouping: {
                    icon_plus: "glyphicon-triangle-right",
                    icon_minus: "glyphicon-triangle-bottom"
                },
                filter: {
                    table_widget: "table table-condensed",
                    srSelect: "form-control",
                    srInput: "form-control",
                    menu_widget: "",
                    icon_search: "glyphicon-search",
                    icon_reset: "glyphicon-refresh",
                    icon_query: "glyphicon-comment"
                },
                subgrid: {
                    icon_plus: "glyphicon-triangle-right",
                    icon_minus: "glyphicon-triangle-bottom",
                    icon_open: "glyphicon-indent-left"
                },
                treegrid: {
                    icon_plus: "glyphicon-triangle-right",
                    icon_minus: "glyphicon-triangle-bottom",
                    icon_leaf: "glyphicon-unchecked"
                },
                fmatter: {
                    icon_edit: "glyphicon-edit",
                    icon_add: "glyphicon-plus",
                    icon_save: "glyphicon-save",
                    icon_cancel: "glyphicon-remove-circle",
                    icon_del: "glyphicon-trash"
                },
                colmenu: {
                    menu_widget: "",
                    input_checkbox: "",
                    filter_select: "form-control",
                    filter_input: "form-control",
                    icon_menu: "glyphicon-menu-hamburger",
                    icon_sort_asc: "glyphicon-sort-by-alphabet",
                    icon_sort_desc: "glyphicon-sort-by-alphabet-alt",
                    icon_columns: "glyphicon-list-alt",
                    icon_filter: "glyphicon-filter",
                    icon_group: "glyphicon-align-left",
                    icon_freeze: "glyphicon-object-align-horizontal",
                    icon_move: "glyphicon-move"
                }
            }
        }
    }), $.fn.jqGrid = function (a) {
        if ("string" == typeof
        a) {
            var
            b = $.jgrid.getMethod(a);
            if (!b) throw "jqGrid - No such method: " + a;
            var
            c = $.makeArray(arguments).slice(1);
            return b.apply(this, c)
        }
        return this.each(function () {
            function
            b(a, b, c, d) {
                if (e.p.multiselect && e.p.multiboxonly || e.p.multimail) if (b) $(e).jqGrid("setSelection", a, d, c);
                else if (e.p.multiboxonly && e.p.multimail) $(e).triggerHandler("jqGridSelectRow", [a, !1, c]), e.p.onSelectRow && e.p.onSelectRow.call(e, a, !1, c);
                else {
                    var
                    f = e.p.frozenColumns ? e.p.id + "_frozen" : "";
                    $(e.p.selarrrow).each(function (a, b) {
                        var
                        c = $(e).jqGrid("getGridRowById", b);
                        c && $(c).removeClass(o), $("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + $.jgrid.jqID(b))[e.p.useProp ? "prop" : "attr"]("checked", !1), f && ($("#" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(f)).removeClass(o), $("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(f))[e.p.useProp ? "prop" : "attr"]("checked", !1))
                    }), e.p.selarrrow = [], $(e).jqGrid("setSelection", a, d, c)
                } else $(e).jqGrid("setSelection", a, d, c)
            }
            if (!this.grid) {
                var
                c;
                null != a && void
                0 !== a.data && (c = a.data, a.data = []);
                var
                d = $.extend(!0, {
                    url: "",
                    height: 150,
                    page: 1,
                    rowNum: 20,
                    rowTotal: null,
                    records: 0,
                    pager: "",
                    pgbuttons: !0,
                    pginput: !0,
                    colModel: [],
                    rowList: [],
                    colNames: [],
                    sortorder: "asc",
                    sortname: "",
                    datatype: "xml",
                    mtype: "GET",
                    altRows: !1,
                    selarrrow: [],
                    savedRow: [],
                    shrinkToFit: !0,
                    xmlReader: {},
                    jsonReader: {},
                    subGrid: !1,
                    subGridModel: [],
                    reccount: 0,
                    lastpage: 0,
                    lastsort: 0,
                    selrow: null,
                    beforeSelectRow: null,
                    onSelectRow: null,
                    onSortCol: null,
                    ondblClickRow: null,
                    onRightClickRow: null,
                    onPaging: null,
                    onSelectAll: null,
                    onInitGrid: null,
                    loadComplete: null,
                    gridComplete: null,
                    loadError: null,
                    loadBeforeSend: null,
                    afterInsertRow: null,
                    beforeRequest: null,
                    beforeProcessing: null,
                    onHeaderClick: null,
                    viewrecords: !1,
                    loadonce: !1,
                    multiselect: !1,
                    multikey: !1,
                    multiboxonly: !1,
                    multimail: !1,
                    multiselectWidth: 30,
                    editurl: null,
                    search: !1,
                    caption: "",
                    hidegrid: !0,
                    hiddengrid: !1,
                    postData: {},
                    userData: {},
                    treeGrid: !1,
                    treeGridModel: "nested",
                    treeReader: {},
                    treeANode: -1,
                    ExpandColumn: null,
                    tree_root_level: 0,
                    prmNames: {
                        page: "page",
                        rows: "rows",
                        sort: "sidx",
                        order: "sord",
                        search: "_search",
                        nd: "nd",
                        id: "id",
                        oper: "oper",
                        editoper: "edit",
                        addoper: "add",
                        deloper: "del",
                        subgridid: "id",
                        npage: null,
                        totalrows: "totalrows"
                    },
                    forceFit: !1,
                    gridstate: "visible",
                    cellEdit: !1,
                    cellsubmit: "remote",
                    nv: 0,
                    loadui: "enable",
                    toolbar: [!1, ""],
                    scroll: !1,
                    deselectAfterSort: !0,
                    scrollrows: !1,
                    autowidth: !1,
                    scrollOffset: 18,
                    cellLayout: 5,
                    subGridWidth: 20,
                    gridview: !0,
                    rownumWidth: 35,
                    rownumbers: !1,
                    pagerpos: "center",
                    recordpos: "right",
                    footerrow: !1,
                    userDataOnFooter: !1,
                    hoverrows: !0,
                    viewsortcols: [!1, "vertical", !0],
                    resizeclass: "",
                    autoencode: !1,
                    remapColumns: [],
                    ajaxGridOptions: {},
                    direction: "ltr",
                    toppager: !1,
                    headertitles: !1,
                    scrollTimeout: 40,
                    data: [],
                    _index: {},
                    grouping: !1,
                    groupingView: {
                        groupField: [],
                        groupOrder: [],
                        groupText: [],
                        groupColumnShow: [],
                        groupSummary: [],
                        showSummaryOnHide: !1,
                        sortitems: [],
                        sortnames: [],
                        summary: [],
                        summaryval: [],
                        plusicon: "",
                        minusicon: "",
                        displayField: [],
                        groupSummaryPos: [],
                        formatDisplayField: [],
                        _locgr: !1
                    },
                    ignoreCase: !0,
                    cmTemplate: {},
                    idPrefix: "",
                    multiSort: !1,
                    minColWidth: 33,
                    scrollPopUp: !1,
                    scrollTopOffset: 0,
                    scrollLeftOffset: "100%",
                    scrollMaxBuffer: 0,
                    storeNavOptions: !1,
                    regional: "en",
                    styleUI: "jQueryUI",
                    responsive: !1,
                    restoreCellonFail: !0,
                    colFilters: {},
                    colMenu: !1
                }, $.jgrid.defaults, a);
                void
                0 !== c && (d.data = c, a.data = c);
                var
                e = this,
                    f = {
                        headers: [],
                        cols: [],
                        footers: [],
                        dragStart: function (a, b, c) {
                            var
                            f = $(this.bDiv).offset().left;
                            this.resizing = {
                                idx: a,
                                startX: b.pageX,
                                sOL: b.pageX - f
                            }, this.hDiv.style.cursor = "col-resize", this.curGbox = $("#rs_m" + $.jgrid.jqID(d.id), "#gbox_" + $.jgrid.jqID(d.id)), this.curGbox.css({
                                display: "block",
                                left: b.pageX - f,
                                top: c[1],
                                height: c[2]
                            }), $(e).triggerHandler("jqGridResizeStart", [b, a]), $.isFunction(d.resizeStart) && d.resizeStart.call(e, b, a), document.onselectstart = function () {
                                return !1
                            }
                        },
                        dragMove: function (a) {
                            if (this.resizing) {
                                var
                                b, c, e = a.pageX - this.resizing.startX,
                                    f = this.headers[this.resizing.idx],
                                    g = "ltr" === d.direction ? f.width + e : f.width - e;
                                g > 33 && (this.curGbox.css({
                                    left: this.resizing.sOL + e
                                }), !0 === d.forceFit ? (b = this.headers[this.resizing.idx + d.nv], (c = "ltr" === d.direction ? b.width - e : b.width + e) > d.minColWidth && (f.newWidth = g, b.newWidth = c)) : (this.newWidth = "ltr" === d.direction ? d.tblwidth + e : d.tblwidth - e, f.newWidth = g))
                            }
                        },
                        dragEnd: function (a) {
                            if (this.hDiv.style.cursor = "default", this.resizing) {
                                var
                                b = this.resizing.idx,
                                    c = this.headers[b].newWidth || this.headers[b].width;
                                c = parseInt(c, 10), this.resizing = !1, $("#rs_m" + $.jgrid.jqID(d.id)).css("display", "none"), d.colModel[b].width = c, this.headers[b].width = c, this.headers[b].el.style.width = c + "px", this.cols[b].style.width = c + "px", this.footers.length > 0 && (this.footers[b].style.width = c + "px"), !0 === d.forceFit ? (c = this.headers[b + d.nv].newWidth || this.headers[b + d.nv].width, this.headers[b + d.nv].width = c, this.headers[b + d.nv].el.style.width = c + "px", this.cols[b + d.nv].style.width = c + "px", this.footers.length > 0 && (this.footers[b + d.nv].style.width = c + "px"), d.colModel[b + d.nv].width = c) : (d.tblwidth = this.newWidth || d.tblwidth, $("table:first", this.bDiv).css("width", d.tblwidth + "px"), $("table:first", this.hDiv).css("width", d.tblwidth + "px"), this.hDiv.scrollLeft = this.bDiv.scrollLeft, d.footerrow && ($("table:first", this.sDiv).css("width", d.tblwidth + "px"), this.sDiv.scrollLeft = this.bDiv.scrollLeft)), a && ($(e).triggerHandler("jqGridResizeStop", [c, b]), $.isFunction(d.resizeStop) && d.resizeStop.call(e, c, b))
                            }
                            this.curGbox = null, document.onselectstart = function () {
                                return !0
                            }
                        },
                        populateVisible: function () {
                            f.timer && clearTimeout(f.timer), f.timer = null;
                            var
                            a = $(f.bDiv).height();
                            if (a) {
                                var
                                b, c, g = $("table:first", f.bDiv);
                                if (g[0].rows.length) try {
                                    b = g[0].rows[1], c = b ? $(b).outerHeight() || f.prevRowHeight : f.prevRowHeight
                                } catch (a) {
                                    c = f.prevRowHeight
                                }
                                if (c) {
                                    f.prevRowHeight = c;
                                    var
                                    h, i, j, k = d.rowNum,
                                        l = f.scrollTop = f.bDiv.scrollTop,
                                        m = Math.round(g.position().top) - l,
                                        n = m + g.height(),
                                        o = c * k;
                                    if (n < a && m <= 0 && (void
                                    0 === d.lastpage || (parseInt((n + l + o - 1) / o, 10) || 0) <= d.lastpage) && (i = parseInt((a - n + o - 1) / o, 10) || 1, n >= 0 || i < 2 || !0 === d.scroll ? (h = (Math.round((n + l) / o) || 0) + 1, m = -1) : m = 1), m > 0 && (h = (parseInt(l / o, 10) || 0) + 1, i = (parseInt((l + a) / o, 10) || 0) + 2 - h, j = !0), i) {
                                        if (d.lastpage && (h > d.lastpage || 1 === d.lastpage || h === d.page && h === d.lastpage)) return;
                                        f.hDiv.loading ? f.timer = setTimeout(f.populateVisible, d.scrollTimeout) : (d.page = h, d.scrollMaxBuffer > 0 && (k > 0 && d.scrollMaxBuffer < k && (d.scrollMaxBuffer = k + 1), d.reccount > d.scrollMaxBuffer - (k > 0 ? k : 0) && (j = !0)), j && (f.selectionPreserver(g[0]), f.emptyRows.call(g[0], !1, !1)), f.populate(i)), d.scrollPopUp && null != d.lastpage && ($("#scroll_g" + d.id).show().html($.jgrid.template($.jgrid.getRegional(e, "defaults.pgtext", d.pgtext), d.page, d.lastpage)).css({
                                            top: d.scrollTopOffset + l * ((parseInt(d.height, 10) - 45) / (parseInt(c, 10) * parseInt(d.records, 10))) + "px",
                                            left: d.scrollLeftOffset
                                        }), $(this).mouseout(function () {
                                            $("#scroll_g" + d.id).hide()
                                        }))
                                    }
                                }
                            }
                        },
                        scrollGrid: function (a) {
                            if (d.scroll) {
                                var
                                b = f.bDiv.scrollTop;
                                void
                                0 === f.scrollTop && (f.scrollTop = 0), b !== f.scrollTop && (f.scrollTop = b, f.timer && clearTimeout(f.timer), f.timer = setTimeout(f.populateVisible, d.scrollTimeout))
                            }
                            f.hDiv.scrollLeft = f.bDiv.scrollLeft, d.footerrow && (f.sDiv.scrollLeft = f.bDiv.scrollLeft), d.frozenColumns && $(f.fbDiv).scrollTop(f.bDiv.scrollTop), a && a.stopPropagation()
                        },
                        selectionPreserver: function (a) {
                            var
                            b = a.p,
                                c = b.selrow,
                                d = b.selarrrow ? $.makeArray(b.selarrrow) : null,
                                e = a.grid.bDiv.scrollLeft,
                                f = function () {
                                    var
                                    g;
                                    if (b.selrow = null, b.selarrrow = [], b.multiselect && d && d.length > 0) for (g = 0; g < d.length; g++) d[g] !== c && $(a).jqGrid("setSelection", d[g], !1, null);
                                    c && $(a).jqGrid("setSelection", c, !1, null), a.grid.bDiv.scrollLeft = e, $(a).off(".selectionPreserver", f)
                                };
                            $(a).on("jqGridGridComplete.selectionPreserver", f)
                        }
                    };
                if ("TABLE" !== this.tagName.toUpperCase() || null == this.id) return void
                alert("Element is not a table or has no id!");
                if (void
                0 !== document.documentMode && document.documentMode <= 5) return void
                alert("Grid can not be used in this ('quirks') mode!");
                var
                g, h, i, j = 0;
                for (h in $.jgrid.regional) $.jgrid.regional.hasOwnProperty(h) && (0 === j && (g = h), j++);
                if (1 === j && g !== d.regional && (d.regional = g), $(this).empty().attr("tabindex", "0"), this.p = d, this.p.useProp = !! $.fn.prop, 0 === this.p.colNames.length) for (j = 0; j < this.p.colModel.length; j++) this.p.colNames[j] = this.p.colModel[j].label || this.p.colModel[j].name;
                if (this.p.colNames.length !== this.p.colModel.length) return void
                alert($.jgrid.getRegional(this, "errors.model"));
                var
                k, l = $.jgrid.getMethod("getStyleUI"),
                    m = e.p.styleUI + ".common",
                    n = l(m, "disabled", !0),
                    o = l(m, "highlight", !0),
                    p = l(m, "hover", !0),
                    q = l(m, "cornerall", !0),
                    r = l(m, "icon_base", !0),
                    s = $.jgrid.styleUI[e.p.styleUI || "jQueryUI"].colmenu,
                    t = $.jgrid.msie(),
                    u = [],
                    v = [],
                    w = [];
                m = e.p.styleUI + ".base", k = $("<div " + l(m, "viewBox", !1, "ui-jqgrid-view") + " role='grid'></div>"), e.p.direction = $.trim(e.p.direction.toLowerCase()), e.p._ald = !1, -1 === $.inArray(e.p.direction, ["ltr", "rtl"]) && (e.p.direction = "ltr"), i = e.p.direction, $(k).insertBefore(this), $(this).appendTo(k);
                var
                x = $("<div " + l(m, "entrieBox", !1, "ui-jqgrid") + "></div>");
                $(x).attr({
                    id: "gbox_" + this.id,
                    dir: i
                }).insertBefore(k), $(k).attr("id", "gview_" + this.id).appendTo(x), $("<div " + l(e.p.styleUI + ".common", "overlay", !1, "jqgrid-overlay") + " id='lui_" + this.id + "'></div>").insertBefore(k), $("<div " + l(m, "loadingBox", !1, "loading") + " id='load_" + this.id + "'>" + $.jgrid.getRegional(e, "defaults.loadtext", this.p.loadtext) + "</div>").insertBefore(k), $(this).attr({
                    role: "presentation",
                    "aria-multiselectable": !! this.p.multiselect,
                    "aria-labelledby": "gbox_" + this.id
                });
                var
                y, z = ["shiftKey", "altKey", "ctrlKey"],
                    A = function (a, b) {
                        return a = parseInt(a, 10), isNaN(a) ? b || 0 : a
                    }, B = function (a, b, c, d, g, h) {
                        var
                        i, j, k = e.p.colModel[a],
                            l = k.align,
                            m = 'style="',
                            n = k.classes,
                            o = k.name,
                            p = [];
                        return l && (m += "text-align:" + l + ";"), !0 === k.hidden && (m += "display:none;"), 0 === b ? m += "width: " + f.headers[a].width + "px;" : ($.isFunction(k.cellattr) || "string" == typeof
                        k.cellattr && null != $.jgrid.cellattr && $.isFunction($.jgrid.cellattr[k.cellattr])) && (i = $.isFunction(k.cellattr) ? k.cellattr : $.jgrid.cellattr[k.cellattr], (j = i.call(e, g, c, d, k, h)) && "string" == typeof
                        j && (j = j.replace(/style/i, "style").replace(/title/i, "title"), j.indexOf("title") > -1 && (k.title = !1), j.indexOf("class") > -1 && (n = void
                        0), p = j.replace(/\-style/g, "-sti").split(/style/), 2 === p.length ? (p[1] = $.trim(p[1].replace(/\-sti/g, "-style").replace("=", "")), 0 !== p[1].indexOf("'") && 0 !== p[1].indexOf('"') || (p[1] = p[1].substring(1)), m += p[1].replace(/'/gi, '"')) : m += '"')), p.length || (p[0] = "", m += '"'), m += (void
                        0 !== n ? ' class="' + n + '"' : "") + (k.title && c ? ' title="' + $.jgrid.stripHtml(c) + '"' : ""), (m += ' aria-describedby="' + e.p.id + "_" + o + '"') + p[0]
                    }, C = function (a) {
                        return null == a || "" === a ? "&#160;" : e.p.autoencode ? $.jgrid.htmlEncode(a) : String(a)
                    }, D = function (a, b, c, d, f) {
                        var
                        g, h = e.p.colModel[c];
                        if (void
                        0 !== h.formatter) {
                            a = "" !== String(e.p.idPrefix) ? $.jgrid.stripPref(e.p.idPrefix, a) : a;
                            var
                            i = {
                                rowId: a,
                                colModel: h,
                                gid: e.p.id,
                                pos: c,
                                styleUI: e.p.styleUI
                            };
                            g = $.isFunction(h.formatter) ? h.formatter.call(e, b, i, d, f) : $.fmatter ? $.fn.fmatter.call(e, h.formatter, b, i, d, f) : C(b)
                        } else g = C(b);
                        return g
                    }, E = function (a, b, c, d, e, f) {
                        var
                        g;
                        return g = D(a, b, c, e, "add"), '<td role="gridcell" ' + B(c, d, g, e, a, f) + ">" + g + "</td>"
                    }, F = function (a, b, c, d, f) {
                        var
                        g = '<input role="checkbox" type="checkbox" id="jqg_' + e.p.id + "_" + a + '" ' + f + ' name="jqg_' + e.p.id + "_" + a + '"' + (d ? 'checked="checked"' : "") + "/>";
                        return '<td role="gridcell" ' + B(b, c, "", null, a, !0) + ">" + g + "</td>"
                    }, G = function (a, b, c, d, e) {
                        var
                        f = (parseInt(c, 10) - 1) * parseInt(d, 10) + 1 + b;
                        return '<td role="gridcell" ' + e + " " + B(a, b, f, null, b, !0) + ">" + f + "</td>"
                    }, H = function (a) {
                        var
                        b, c, d = [],
                            f = 0;
                        for (c = 0; c < e.p.colModel.length; c++) b = e.p.colModel[c], "cb" !== b.name && "subgrid" !== b.name && "rn" !== b.name && (d[f] = "local" === a ? b.name : "xml" === a || "xmlstring" === a ? b.xmlmap || b.name : b.jsonmap || b.name, !1 !== e.p.keyName && !0 === b.key && (e.p.keyName = d[f], e.p.keyIndex = f), f++);
                        return d
                    }, I = function (a) {
                        var
                        b = e.p.remapColumns;
                        return b && b.length || (b = $.map(e.p.colModel, function (a, b) {
                            return b
                        })), a && (b = $.map(b, function (b) {
                            return b < a ? null : b - a
                        })), b
                    }, J = function (a, b) {
                        var
                        c;
                        this.p.deepempty ? $(this.rows).slice(1).remove() : (c = this.rows.length > 0 ? this.rows[0] : null, $(this.firstChild).empty().append(c)), a && this.p.scroll && ($(this.grid.bDiv.firstChild).css({
                            height: "auto"
                        }), $(this.grid.bDiv.firstChild.firstChild).css({
                            height: "0px",
                            display: "none"
                        }), 0 !== this.grid.bDiv.scrollTop && (this.grid.bDiv.scrollTop = 0)), !0 === b && this.p.treeGrid && !this.p.loadonce && (this.p.data = [], this.p._index = {})
                    }, K = function () {
                        var
                        a, b, c, d, f, g, h, i, j, k, l, m = e.p,
                            n = m.data,
                            o = n.length,
                            p = m.localReader,
                            q = m.colModel,
                            r = p.cell,
                            s = (!0 === m.multiselect ? 1 : 0) + (!0 === m.subGrid ? 1 : 0) + (!0 === m.rownumbers ? 1 : 0),
                            t = m.scroll ? $.jgrid.randId() : 1;
                        if ("local" === m.datatype && !0 === p.repeatitems) for (j = I(s), k = H("local"), d = !1 === m.keyName ? $.isFunction(p.id) ? p.id.call(e, n) : p.id : m.keyName, a = 0; a < o; a++) {
                            for (c = n[a], f = $.jgrid.getAccessor(c, d), void
                            0 === f && ("number" == typeof
                            d && null != q[d + s] && (f = $.jgrid.getAccessor(c, q[d + s].name)), void
                            0 === f && (f = t + a, r && (g = $.jgrid.getAccessor(c, r) || c, f = null != g && void
                            0 !== g[d] ? g[d] : f, g = null))), i = {}, i[p.id] = f, r && (c = $.jgrid.getAccessor(c, r) || c), l = $.isArray(c) ? j : k, b = 0; b < l.length; b++) h = $.jgrid.getAccessor(c, l[b]), i[q[b + s].name] = h;
                            n[a] = i
                        }
                    }, L = function () {
                        var
                        a, b, c, d = e.p.data.length;
                        for (a = !1 === e.p.keyName || !0 === e.p.loadonce ? e.p.localReader.id : e.p.keyName, e.p._index = [], b = 0; b < d; b++) c = $.jgrid.getAccessor(e.p.data[b], a), void
                        0 === c && (c = String(b + 1)), e.p._index[c] = b
                    }, M = function (a, b, c, d, f) {
                        var
                        g, h = "-1",
                            i = "",
                            j = b ? "display:none;" : "",
                            k = $(e).triggerHandler("jqGridRowAttr", [d, f, a]);
                        if ("object" != typeof
                        k && (k = $.isFunction(e.p.rowattr) ? e.p.rowattr.call(e, d, f, a) : "string" == typeof
                        e.p.rowattr && null != $.jgrid.rowattr && $.isFunction($.jgrid.rowattr[e.p.rowattr]) ? $.jgrid.rowattr[e.p.rowattr].call(e, d, f, a) : {}), !$.isEmptyObject(k)) {
                            k.hasOwnProperty("id") && (a = k.id, delete
                            k.id), k.hasOwnProperty("tabindex") && (h = k.tabindex, delete
                            k.tabindex), k.hasOwnProperty("style") && (j += k.style, delete
                            k.style), k.hasOwnProperty("class") && (c += " " + k.class, delete
                            k.class);
                            try {
                                delete
                                k.role
                            } catch (a) {}
                            for (g in k) k.hasOwnProperty(g) && (i += " " + g + "=" + k[g])
                        }
                        return '<tr role="row" id="' + a + '" tabindex="' + h + '" class="' + c + '"' + ("" === j ? "" : ' style="' + j + '"') + i + ">"
                    }, N = function (a, b, c, d) {
                        var
                        f = new
                        Date,
                            g = "local" !== e.p.datatype && e.p.loadonce || "xmlstring" === e.p.datatype,
                            h = "_id_",
                            i = e.p.xmlReader,
                            j = "local" === e.p.datatype ? "local" : "xml";
                        if (g && (e.p.data = [], e.p._index = {}, e.p.localReader.id = h), e.p.reccount = 0, $.isXMLDoc(a)) {
                            -1 !== e.p.treeANode || e.p.scroll ? b = b > 1 ? b : 1 : (J.call(e, !1, !0), b = 1);
                            var
                            k, n, o, p, q, r, s, t, u, v = $(e),
                                w = 0,
                                x = !0 === e.p.multiselect ? 1 : 0,
                                y = 0,
                                z = !0 === e.p.rownumbers ? 1 : 0,
                                B = [],
                                C = {}, D = [],
                                K = l(m, "rowBox", !0, "jqgrow ui-row-" + e.p.direction);
                            !0 === e.p.subGrid && (y = 1, p = $.jgrid.getMethod("addSubGridCell")), i.repeatitems || (B = H(j)), q = !1 === e.p.keyName ? $.isFunction(i.id) ? i.id.call(e, a) : i.id : e.p.keyName, i.repeatitems && e.p.keyName && isNaN(q) && (q = e.p.keyIndex), r = -1 === String(q).indexOf("[") ? B.length ? function (a, b) {
                                return $(q, a).text() || b
                            } : function (a, b) {
                                return $(i.cell, a).eq(q).text() || b
                            } : function (a, b) {
                                return a.getAttribute(q.replace(/[\[\]]/g, "")) || b
                            }, e.p.userData = {}, e.p.page = A($.jgrid.getXmlData(a, i.page), e.p.page), e.p.lastpage = A($.jgrid.getXmlData(a, i.total), 1), e.p.records = A($.jgrid.getXmlData(a, i.records)), $.isFunction(i.userdata) ? e.p.userData = i.userdata.call(e, a) || {} : $.jgrid.getXmlData(a, i.userdata, !0).each(function () {
                                e.p.userData[this.getAttribute("name")] = $(this).text()
                            });
                            var
                            L = $.jgrid.getXmlData(a, i.root, !0);
                            L = $.jgrid.getXmlData(L, i.row, !0), L || (L = []);
                            var
                            N, O = L.length,
                                P = 0,
                                Q = [],
                                R = parseInt(e.p.rowNum, 10),
                                S = e.p.scroll ? $.jgrid.randId() : 1,
                                T = $(e).find("tbody:first"),
                                U = !1;
                            if (e.p.grouping && (U = !0 === e.p.groupingView.groupCollapse, N = $.jgrid.getMethod("groupingPrepare")), O > 0 && e.p.page <= 0 && (e.p.page = 1), L && O) {
                                d && (R *= d + 1);
                                for (var
                                V = $.isFunction(e.p.afterInsertRow), W = z ? l(m, "rownumBox", !1, "jqgrid-rownum") : "", X = x ? l(m, "multiBox", !1, "cbox") : ""; P < O;) {
                                    t = L[P], u = r(t, S + P), u = e.p.idPrefix + u;
                                    var
                                    Y = D.length;
                                    if (D.push(""), z && D.push(G(0, P, e.p.page, e.p.rowNum, W)), x && D.push(F(u, z, P, !1, X)), y && D.push(p.call(v, x + z, P + b)), i.repeatitems) {
                                        s || (s = I(x + y + z));
                                        var
                                        Z = $.jgrid.getXmlData(t, i.cell, !0);
                                        $.each(s, function (a) {
                                            var
                                            c = Z[this];
                                            if (!c) return !1;
                                            o = c.textContent || c.text, C[e.p.colModel[a + x + y + z].name] = o, D.push(E(u, o, a + x + y + z, P + b, t, C))
                                        })
                                    } else for (k = 0; k < B.length; k++) o = $.jgrid.getXmlData(t, B[k]), C[e.p.colModel[k + x + y + z].name] = o, D.push(E(u, o, k + x + y + z, P + b, t, C));
                                    if (D[Y] = M(u, U, K, C, t), D.push("</tr>"), e.p.grouping && (Q.push(D), e.p.groupingView._locgr || N.call(v, C, P), D = []), (g || !0 === e.p.treeGrid && !e.p._ald) && (C[h] = $.jgrid.stripPref(e.p.idPrefix, u), e.p.data.push(C), e.p._index[C[h]] = e.p.data.length - 1), !1 === e.p.gridview && (T.append(D.join("")), v.triggerHandler("jqGridAfterInsertRow", [u, C, t]), V && e.p.afterInsertRow.call(e, u, C, t), D = []), C = {}, w++, P++, w === R) break
                                }
                            }
                            if (!0 === e.p.gridview && (n = e.p.treeANode > -1 ? e.p.treeANode : 0, e.p.grouping ? g || (v.jqGrid("groupingRender", Q, e.p.colModel.length, e.p.page, R), Q = null) : !0 === e.p.treeGrid && n > 0 ? $(e.rows[n]).after(D.join("")) : (T.append(D.join("")), e.grid.cols = e.rows[0].cells)), e.p.totaltime = new
                            Date - f, D = null, !0 === e.p.subGrid) try {
                                v.jqGrid("addSubGrid", x + z)
                            } catch (a) {}
                            if (w > 0 && 0 === e.p.records && (e.p.records = O), !0 === e.p.treeGrid) try {
                                v.jqGrid("setTreeNode", n + 1, w + n + 1)
                            } catch (a) {}
                            if (e.p.reccount = w, e.p.treeANode = -1, e.p.userDataOnFooter && v.jqGrid("footerData", "set", e.p.userData, !0), g && (e.p.records = O, e.p.lastpage = Math.ceil(O / R)), c || e.updatepager(!1, !0), g) {
                                for (; w < O;) {
                                    if (t = L[w], u = r(t, w + S), u = e.p.idPrefix + u, i.repeatitems) {
                                        s || (s = I(x + y + z));
                                        var
                                        _ = $.jgrid.getXmlData(t, i.cell, !0);
                                        $.each(s, function (a) {
                                            var
                                            b = _[this];
                                            if (!b) return !1;
                                            o = b.textContent || b.text, C[e.p.colModel[a + x + y + z].name] = o
                                        })
                                    } else for (k = 0; k < B.length; k++) o = $.jgrid.getXmlData(t, B[k]), C[e.p.colModel[k + x + y + z].name] = o;
                                    C[h] = $.jgrid.stripPref(e.p.idPrefix, u), e.p.grouping && N.call(v, C, w), e.p.data.push(C), e.p._index[C[h]] = e.p.data.length - 1, C = {}, w++
                                }
                                e.p.grouping && (e.p.groupingView._locgr = !0, v.jqGrid("groupingRender", Q, e.p.colModel.length, e.p.page, R), Q = null)
                            }
                        }
                    }, O = function (a, b, c, d) {
                        var
                        f = new
                        Date;
                        if (a) {
                            -1 !== e.p.treeANode || e.p.scroll ? b = b > 1 ? b : 1 : (J.call(e, !1, !0), b = 1);
                            var
                            g, h, i = "_id_",
                                j = "local" !== e.p.datatype && e.p.loadonce || "jsonstring" === e.p.datatype;
                            j && (e.p.data = [], e.p._index = {}, e.p.localReader.id = i), e.p.reccount = 0, "local" === e.p.datatype ? (g = e.p.localReader, h = "local") : (g = e.p.jsonReader, h = "json");
                            var
                            k, n, p, q, r, s, t, u, v, w, x, y = $(e),
                                z = 0,
                                B = [],
                                C = e.p.multiselect ? 1 : 0,
                                D = !0 === e.p.subGrid ? 1 : 0,
                                K = !0 === e.p.rownumbers ? 1 : 0,
                                L = I(C + D + K),
                                N = H(h),
                                O = {}, P = [],
                                Q = l(m, "rowBox", !0, "jqgrow ui-row-" + e.p.direction);
                            e.p.page = A($.jgrid.getAccessor(a, g.page), e.p.page), e.p.lastpage = A($.jgrid.getAccessor(a, g.total), 1), e.p.records = A($.jgrid.getAccessor(a, g.records)), e.p.userData = $.jgrid.getAccessor(a, g.userdata) || {}, D && (r = $.jgrid.getMethod("addSubGridCell")), v = !1 === e.p.keyName ? $.isFunction(g.id) ? g.id.call(e, a) : g.id : e.p.keyName, g.repeatitems && e.p.keyName && isNaN(v) && (v = e.p.keyIndex), u = $.jgrid.getAccessor(a, g.root), null == u && $.isArray(a) && (u = a), u || (u = []), t = u.length, n = 0, t > 0 && e.p.page <= 0 && (e.p.page = 1);
                            var
                            R, S = parseInt(e.p.rowNum, 10),
                                T = e.p.scroll ? $.jgrid.randId() : 1,
                                U = !1;
                            d && (S *= d + 1), "local" !== e.p.datatype || e.p.deselectAfterSort || (U = !0);
                            var
                            V, W = $.isFunction(e.p.afterInsertRow),
                                X = [],
                                Y = !1,
                                Z = $(e).find("tbody:first"),
                                _ = K ? l(m, "rownumBox", !1, "jqgrid-rownum") : "",
                                aa = C ? l(m, "multiBox", !1, "cbox") : "";
                            for (e.p.grouping && (Y = !0 === e.p.groupingView.groupCollapse, V = $.jgrid.getMethod("groupingPrepare")); n < t;) {
                                if (q = u[n], void
                                0 === (x = $.jgrid.getAccessor(q, v)) && ("number" == typeof
                                v && null != e.p.colModel[v + C + D + K] && (x = $.jgrid.getAccessor(q, e.p.colModel[v + C + D + K].name)), void
                                0 === x && (x = T + n, 0 === B.length && g.cell))) {
                                    var
                                    ba = $.jgrid.getAccessor(q, g.cell) || q;
                                    x = null != ba && void
                                    0 !== ba[v] ? ba[v] : x, ba = null
                                }
                                x = e.p.idPrefix + x, U && (R = e.p.multiselect ? -1 !== $.inArray(x, e.p.selarrrow) : x === e.p.selrow);
                                var
                                ca = P.length;
                                for (P.push(""), K && P.push(G(0, n, e.p.page, e.p.rowNum, _)), C && P.push(F(x, K, n, R, aa)), D && P.push(r.call(y, C + K, n + b)), s = N, g.repeatitems && (g.cell && (q = $.jgrid.getAccessor(q, g.cell) || q), $.isArray(q) && (s = L)), p = 0; p < s.length; p++) k = $.jgrid.getAccessor(q, s[p]), O[e.p.colModel[p + C + D + K].name] = k, P.push(E(x, k, p + C + D + K, n + b, q, O));
                                if (P[ca] = M(x, Y, R ? Q + " " + o : Q, O, q), P.push("</tr>"), e.p.grouping && (X.push(P), e.p.groupingView._locgr || V.call(y, O, n), P = []), (j || !0 === e.p.treeGrid && !e.p._ald) && (O[i] = $.jgrid.stripPref(e.p.idPrefix, x), e.p.data.push(O), e.p._index[O[i]] = e.p.data.length - 1), !1 === e.p.gridview && (Z.append(P.join("")), y.triggerHandler("jqGridAfterInsertRow", [x, O, q]), W && e.p.afterInsertRow.call(e, x, O, q), P = []), O = {}, z++, n++, z === S) break
                            }
                            if (!0 === e.p.gridview && (w = e.p.treeANode > -1 ? e.p.treeANode : 0, e.p.grouping ? j || (y.jqGrid("groupingRender", X, e.p.colModel.length, e.p.page, S), X = null) : !0 === e.p.treeGrid && w > 0 ? $(e.rows[w]).after(P.join("")) : (Z.append(P.join("")), e.grid.cols = e.rows[0].cells)), e.p.totaltime = new
                            Date - f, P = null, !0 === e.p.subGrid) try {
                                y.jqGrid("addSubGrid", C + K)
                            } catch (a) {}
                            if (z > 0 && 0 === e.p.records && (e.p.records = t), !0 === e.p.treeGrid) try {
                                y.jqGrid("setTreeNode", w + 1, z + w + 1)
                            } catch (a) {}
                            if (e.p.reccount = z, e.p.treeANode = -1, e.p.userDataOnFooter && y.jqGrid("footerData", "set", e.p.userData, !0), j && (e.p.records = t, e.p.lastpage = Math.ceil(t / S)), c || e.updatepager(!1, !0), j) {
                                for (; z < t && u[z];) {
                                    if (q = u[z], void
                                    0 === (x = $.jgrid.getAccessor(q, v)) && ("number" == typeof
                                    v && null != e.p.colModel[v + C + D + K] && (x = $.jgrid.getAccessor(q, e.p.colModel[v + C + D + K].name)), void
                                    0 === x && (x = T + z, 0 === B.length && g.cell))) {
                                        var
                                        da = $.jgrid.getAccessor(q, g.cell) || q;
                                        x = null != da && void
                                        0 !== da[v] ? da[v] : x, da = null
                                    }
                                    if (q) {
                                        for (x = e.p.idPrefix + x, s = N, g.repeatitems && (g.cell && (q = $.jgrid.getAccessor(q, g.cell) || q), $.isArray(q) && (s = L)), p = 0; p < s.length; p++) O[e.p.colModel[p + C + D + K].name] = $.jgrid.getAccessor(q, s[p]);
                                        O[i] = $.jgrid.stripPref(e.p.idPrefix, x), e.p.grouping && V.call(y, O, z), e.p.data.push(O), e.p._index[O[i]] = e.p.data.length - 1, O = {}
                                    }
                                    z++
                                }
                                e.p.grouping && (e.p.groupingView._locgr = !0, y.jqGrid("groupingRender", X, e.p.colModel.length, e.p.page, S), X = null)
                            }
                        }
                    }, P = function (a) {
                        function
                        b(a) {
                            var
                            c, d, f, g, h, i, j = 0;
                            if (null != a.groups) {
                                for (d = a.groups.length && "OR" === a.groupOp.toString().toUpperCase(), d && s.orBegin(), c = 0; c < a.groups.length; c++) {
                                    j > 0 && d && s.or();
                                    try {
                                        b(a.groups[c])
                                    } catch (a) {
                                        alert(a)
                                    }
                                    j++
                                }
                                d && s.orEnd()
                            }
                            if (null != a.rules) try {
                                for (f = a.rules.length && "OR" === a.groupOp.toString().toUpperCase(), f && s.orBegin(), c = 0; c < a.rules.length; c++) h = a.rules[c], g = a.groupOp.toString().toUpperCase(), r[h.op] && h.field && (j > 0 && g && "OR" === g && (s = s.or()), i = k[h.field], "date" === i.stype && i.srcfmt && i.newfmt && i.srcfmt !== i.newfmt && (h.data = $.jgrid.parseDate.call(e, i.newfmt, h.data, i.srcfmt)), s = r[h.op](s, g)(h.field, h.data, k[h.field])), j++;
                                f && s.orEnd()
                            } catch (a) {
                                alert(a)
                            }
                        }
                        var
                        c, d, f, g, h = e.p.multiSort ? [] : "",
                            i = [],
                            j = !1,
                            k = {}, l = [],
                            m = [];
                        if ($.isArray(e.p.data)) {
                            var
                            n, o, p, q = !! e.p.grouping && e.p.groupingView;
                            if ($.each(e.p.colModel, function () {
                                if (d = this.sorttype || "text", p = this.index || this.name, "date" === d || "datetime" === d ? (this.formatter && "string" == typeof
                                this.formatter && "date" === this.formatter ? (c = this.formatoptions && this.formatoptions.srcformat ? this.formatoptions.srcformat : $.jgrid.getRegional(e, "formatter.date.srcformat"), f = this.formatoptions && this.formatoptions.newformat ? this.formatoptions.newformat : $.jgrid.getRegional(e, "formatter.date.newformat")) : c = f = this.datefmt || "Y-m-d", k[p] = {
                                    stype: d,
                                    srcfmt: c,
                                    newfmt: f,
                                    sfunc: this.sortfunc || null
                                }) : k[p] = {
                                    stype: d,
                                    srcfmt: "",
                                    newfmt: "",
                                    sfunc: this.sortfunc || null
                                }, e.p.grouping) for (o = 0, n = q.groupField.length; o < n; o++) this.name === q.groupField[o] && (l[o] = k[p], m[o] = p);
                                e.p.multiSort || j || p !== e.p.sortname || (h = p, j = !0)
                            }), e.p.multiSort && (h = u, i = v), e.p.treeGrid && e.p._sort) return void
                            $(e).jqGrid("SortTree", h, e.p.sortorder, k[h].stype || "text", k[h].srcfmt || "");
                            var
                            r = {
                                eq: function (a) {
                                    return a.equals
                                },
                                ne: function (a) {
                                    return a.notEquals
                                },
                                lt: function (a) {
                                    return a.less
                                },
                                le: function (a) {
                                    return a.lessOrEquals
                                },
                                gt: function (a) {
                                    return a.greater
                                },
                                ge: function (a) {
                                    return a.greaterOrEquals
                                },
                                cn: function (a) {
                                    return a.contains
                                },
                                nc: function (a, b) {
                                    return "OR" === b ? a.orNot().contains : a.andNot().contains
                                },
                                bw: function (a) {
                                    return a.startsWith
                                },
                                bn: function (a, b) {
                                    return "OR" === b ? a.orNot().startsWith : a.andNot().startsWith
                                },
                                en: function (a, b) {
                                    return "OR" === b ? a.orNot().endsWith : a.andNot().endsWith
                                },
                                ew: function (a) {
                                    return a.endsWith
                                },
                                ni: function (a, b) {
                                    return "OR" === b ? a.orNot().equals : a.andNot().equals
                                },
                                in : function (a) {
                                    return a.equals
                                },
                                nu: function (a) {
                                    return a.isNull
                                },
                                nn: function (a, b) {
                                    return "OR" === b ? a.orNot().isNull : a.andNot().isNull
                                }
                            }, s = $.jgrid.from.call(e, e.p.data);
                            if (e.p.ignoreCase && (s = s.ignoreCase()), !0 === e.p.search) {
                                var
                                t = e.p.postData.filters;
                                if (t) "string" == typeof t && (t = $.jgrid.parse(t)), b(t);
                                else try {
                                    g = k[e.p.postData.searchField], "date" === g.stype && g.srcfmt && g.newfmt && g.srcfmt !== g.newfmt && (e.p.postData.searchString = $.jgrid.parseDate.call(e, g.newfmt, e.p.postData.searchString, g.srcfmt)), s = r[e.p.postData.searchOper](s)(e.p.postData.searchField, e.p.postData.searchString, k[e.p.postData.searchField])
                                } catch (a) {}
                            } else e.p.treeGrid && "nested" === e.p.treeGridModel && s.orderBy(e.p.treeReader.left_field, "asc", "integer", "", null);
                            if (e.p.treeGrid && "adjacency" === e.p.treeGridModel && (n = 0, h = null), e.p.grouping) for (o = 0; o < n; o++) s.orderBy(m[o], q.groupOrder[o], l[o].stype, l[o].srcfmt);
                            e.p.multiSort ? $.each(h, function (a) {
                                s.orderBy(this, i[a], k[this].stype, k[this].srcfmt, k[this].sfunc)
                            }) : h && e.p.sortorder && j && ("DESC" === e.p.sortorder.toUpperCase() ? s.orderBy(e.p.sortname, "d", k[h].stype, k[h].srcfmt, k[h].sfunc) : s.orderBy(e.p.sortname, "a", k[h].stype, k[h].srcfmt, k[h].sfunc));
                            var
                            w = s.select(),
                                x = parseInt(e.p.rowNum, 10),
                                y = w.length,
                                z = parseInt(e.p.page, 10),
                                A = Math.ceil(y / x),
                                B = {};
                            if ((e.p.search || e.p.resetsearch) && e.p.grouping && e.p.groupingView._locgr) {
                                e.p.groupingView.groups = [];
                                var
                                C, D, E, F = $.jgrid.getMethod("groupingPrepare");
                                if (e.p.footerrow && e.p.userDataOnFooter) {
                                    for (D in e.p.userData) e.p.userData.hasOwnProperty(D) && (e.p.userData[D] = 0);
                                    E = !0
                                }
                                for (C = 0; C < y; C++) {
                                    if (E) for (D in e.p.userData) e.p.userData.hasOwnProperty(D) && (e.p.userData[D] += parseFloat(w[C][D] || 0));
                                    F.call($(e), w[C], C, x)
                                }
                            }
                            return a ? w : (w = e.p.treeGrid && e.p.search ? $(e).jqGrid("searchTree", w) : w.slice((z - 1) * x, z * x), s = null, k = null, B[e.p.localReader.total] = A, B[e.p.localReader.page] = z, B[e.p.localReader.records] = y, B[e.p.localReader.root] = w, B[e.p.localReader.userdata] = e.p.userData, w = null, B)
                        }
                    }, Q = function (a, b) {
                        var
                        c, d, f, g, h, i, j, k, o = "",
                            q = e.p.pager ? $.jgrid.jqID(e.p.pager.substr(1)) : "",
                            r = q ? "_" + q : "",
                            s = e.p.toppager ? "_" + e.p.toppager.substr(1) : "";
                        if (f = parseInt(e.p.page, 10) - 1, f < 0 && (f = 0), f *= parseInt(e.p.rowNum, 10), h = f + e.p.reccount, e.p.scroll) {
                            var
                            t = $("tbody:first > tr:gt(0)", e.grid.bDiv);
                            h > e.p.records && (h = e.p.records), f = h - t.length, e.p.reccount = t.length;
                            var
                            u = t.outerHeight() || e.grid.prevRowHeight;
                            if (u) {
                                var
                                v = f * u,
                                    w = parseInt(e.p.records, 10) * u;
                                $(">div:first", e.grid.bDiv).css({
                                    height: w
                                }).children("div:first").css({
                                    height: v,
                                    display: v ? "" : "none"
                                }), 0 === e.grid.bDiv.scrollTop && e.p.page > 1 && (e.grid.bDiv.scrollTop = e.p.rowNum * (e.p.page - 1) * u)
                            }
                            e.grid.bDiv.scrollLeft = e.grid.hDiv.scrollLeft
                        }
                        if (o = e.p.pager || "", o += e.p.toppager ? o ? "," + e.p.toppager : e.p.toppager : "") {
                            if (j = $.jgrid.getRegional(e, "formatter.integer"), c = A(e.p.page), d = A(e.p.lastpage), $(".selbox", o)[this.p.useProp ? "prop" : "attr"]("disabled", !1), !0 === e.p.pginput && ($("#input" + r).html($.jgrid.template($.jgrid.getRegional(e, "defaults.pgtext", e.p.pgtext) || "", "<input " + l(m, "pgInput", !1, "ui-pg-input") + " type='text' size='2' maxlength='7' value='0' role='textbox'/>", "<span id='sp_1_" + $.jgrid.jqID(q) + "'></span>")), e.p.toppager && $("#input_t" + s).html($.jgrid.template($.jgrid.getRegional(e, "defaults.pgtext", e.p.pgtext) || "", "<input " + l(m, "pgInput", !1, "ui-pg-input") + " type='text' size='2' maxlength='7' value='0' role='textbox'/>", "<span id='sp_1_" + $.jgrid.jqID(q) + "_toppager'></span>")), $(".ui-pg-input", o).val(e.p.page), k = e.p.toppager ? "#sp_1" + r + ",#sp_1" + r + "_toppager" : "#sp_1" + r, $(k).html($.fmatter ? $.fmatter.util.NumberFormat(e.p.lastpage, j) : e.p.lastpage)), e.p.viewrecords) if (0 === e.p.reccount) $(".ui-paging-info", o).html($.jgrid.getRegional(e, "defaults.emptyrecords", e.p.emptyrecords));
                            else {
                                g = f + 1, i = e.p.records, $.fmatter && (g = $.fmatter.util.NumberFormat(g, j), h = $.fmatter.util.NumberFormat(h, j), i = $.fmatter.util.NumberFormat(i, j));
                                var
                                x = $.jgrid.getRegional(e, "defaults.recordtext", e.p.recordtext);
                                $(".ui-paging-info", o).html($.jgrid.template(x, g, h, i))
                            }!0 === e.p.pgbuttons && (c <= 0 && (c = d = 0), 1 === c || 0 === c ? ($("#first" + r + ", #prev" + r).addClass(n).removeClass(p), e.p.toppager && $("#first_t" + s + ", #prev_t" + s).addClass(n).removeClass(p)) : ($("#first" + r + ", #prev" + r).removeClass(n), e.p.toppager && $("#first_t" + s + ", #prev_t" + s).removeClass(n)), c === d || 0 === c ? ($("#next" + r + ", #last" + r).addClass(n).removeClass(p), e.p.toppager && $("#next_t" + s + ", #last_t" + s).addClass(n).removeClass(p)) : ($("#next" + r + ", #last" + r).removeClass(n), e.p.toppager && $("#next_t" + s + ", #last_t" + s).removeClass(n)))
                        }!0 === a && !0 === e.p.rownumbers && $(">td.jqgrid-rownum", e.rows).each(function (a) {
                            $(this).html(f + 1 + a)
                        }), b && e.p.jqgdnd && $(e).jqGrid("gridDnD", "updateDnD"), $(e).triggerHandler("jqGridGridComplete"), $.isFunction(e.p.gridComplete) && e.p.gridComplete.call(e), $(e).triggerHandler("jqGridAfterGridComplete")
                    }, R = function () {
                        e.grid.hDiv.loading = !0, e.p.hiddengrid || $(e).jqGrid("progressBar", {
                            method: "show",
                            loadtype: e.p.loadui,
                            htmlcontent: $.jgrid.getRegional(e, "defaults.loadtext", e.p.loadtext)
                        })
                    }, S = function () {
                        e.grid.hDiv.loading = !1, $(e).jqGrid("progressBar", {
                            method: "hide",
                            loadtype: e.p.loadui
                        })
                    }, T = function (a, b, c) {
                        var
                        d = $(e).triggerHandler("jqGridBeforeProcessing", [a, b, c]);
                        return d = void
                        0 === d || "boolean" != typeof
                        d || d, $.isFunction(e.p.beforeProcessing) && !1 === e.p.beforeProcessing.call(e, a, b, c) && (d = !1), d
                    }, U = function (a, b) {
                        $(e).triggerHandler("jqGridLoadComplete", [a]), b && e.p.loadComplete.call(e, a), $(e).triggerHandler("jqGridAfterLoadComplete", [a]), e.p.datatype = "local", e.p.datastr = null, S()
                    }, V = function (a) {
                        if (!e.grid.hDiv.loading) {
                            var
                            b, c, d = e.p.scroll && !1 === a,
                                f = {}, g = e.p.prmNames;
                            e.p.page <= 0 && (e.p.page = Math.min(1, e.p.lastpage)), null !== g.search && (f[g.search] = e.p.search), null !== g.nd && (f[g.nd] = (new
                            Date).getTime()), null !== g.rows && (f[g.rows] = e.p.rowNum), null !== g.page && (f[g.page] = e.p.page), null !== g.sort && (f[g.sort] = e.p.sortname), null !== g.order && (f[g.order] = e.p.sortorder), null !== e.p.rowTotal && null !== g.totalrows && (f[g.totalrows] = e.p.rowTotal);
                            var
                            h = $.isFunction(e.p.loadComplete),
                                i = h ? e.p.loadComplete : null,
                                j = 0;
                            if (a = a || 1, a > 1 ? null !== g.npage ? (f[g.npage] = a, j = a - 1, a = 1) : i = function (b) {
                                e.p.page++, e.grid.hDiv.loading = !1, h && e.p.loadComplete.call(e, b), V(a - 1)
                            } : null !== g.npage && delete
                            e.p.postData[g.npage], e.p.grouping) {
                                $(e).jqGrid("groupingSetup");
                                var
                                k, l = e.p.groupingView,
                                    m = "";
                                for (k = 0; k < l.groupField.length; k++) {
                                    var
                                    n = l.groupField[k];
                                    $.each(e.p.colModel, function (a, b) {
                                        b.name === n && b.index && (n = b.index)
                                    }), m += n + " " + l.groupOrder[k] + ", "
                                }
                                f[g.sort] = m + f[g.sort]
                            }
                            $.extend(e.p.postData, f);
                            var
                            o = e.p.scroll ? e.rows.length - 1 : 1;
                            if ($.isFunction(e.p.datatype)) return void
                            e.p.datatype.call(e, e.p.postData, "load_" + e.p.id, o, a, j);
                            var
                            p = $(e).triggerHandler("jqGridBeforeRequest");
                            if (!1 === p || "stop" === p) return;
                            if ($.isFunction(e.p.beforeRequest) && (!1 === (p = e.p.beforeRequest.call(e)) || "stop" === p)) return;
                            switch (b = e.p.datatype.toLowerCase()) {
                                case "json":
                                case "jsonp":
                                case "xml":
                                case "script":
                                    $.ajax($.extend({
                                        url: e.p.url,
                                        type: e.p.mtype,
                                        dataType: b,
                                        data: $.isFunction(e.p.serializeGridData) ? e.p.serializeGridData.call(e, e.p.postData) : e.p.postData,
                                        success: function (c, f, g) {
                                            if (!T(c, f, g)) return void
                                            S();
                                            "xml" === b ? N(c, o, a > 1, j) : O(c, o, a > 1, j), $(e).triggerHandler("jqGridLoadComplete", [c]), i && i.call(e, c), $(e).triggerHandler("jqGridAfterLoadComplete", [c]), d && e.grid.populateVisible(), (e.p.loadonce || e.p.treeGrid) && (e.p.datatype = "local"), c = null, 1 === a && S()
                                        },
                                        error: function (b, c, d) {
                                            $(e).triggerHandler("jqGridLoadError", [b, c, d]), $.isFunction(e.p.loadError) && e.p.loadError.call(e, b, c, d), 1 === a && S(), b = null
                                        },
                                        beforeSend: function (a, b) {
                                            var
                                            c = !0;
                                            if (c = $(e).triggerHandler("jqGridLoadBeforeSend", [a, b]), $.isFunction(e.p.loadBeforeSend) && (c = e.p.loadBeforeSend.call(e, a, b)), void
                                            0 === c && (c = !0), !1 === c) return !1;
                                            R()
                                        }
                                    }, $.jgrid.ajaxOptions, e.p.ajaxGridOptions));
                                    break;
                                case "xmlstring":
                                    if (R(), c = "string" != typeof
                                    e.p.datastr ? e.p.datastr : $.parseXML(e.p.datastr), !T(c, 200, null)) return void
                                    S();
                                    N(c), U(c, h);
                                    break;
                                case "jsonstring":
                                    if (R(), c = "string" == typeof
                                    e.p.datastr ? $.jgrid.parse(e.p.datastr) : e.p.datastr, !T(c, 200, null)) return void
                                    S();
                                    O(c), U(c, h);
                                    break;
                                case "local":
                                case "clientside":
                                    R(), e.p.datatype = "local", e.p._ald = !0;
                                    var
                                    q = P(!1);
                                    if (!T(q, 200, null)) return void
                                    S();
                                    O(q, o, a > 1, j), $(e).triggerHandler("jqGridLoadComplete", [q]), i && i.call(e, q), $(e).triggerHandler("jqGridAfterLoadComplete", [q]), d && e.grid.populateVisible(), S(), e.p._ald = !1
                            }
                            e.p._sort = !1
                        }
                    }, W = function (a) {
                        $("#cb_" + $.jgrid.jqID(e.p.id), e.grid.hDiv)[e.p.useProp ? "prop" : "attr"]("checked", a), (e.p.frozenColumns ? e.p.id + "_frozen" : "") && $("#cb_" + $.jgrid.jqID(e.p.id), e.grid.fhDiv)[e.p.useProp ? "prop" : "attr"]("checked", a)
                    }, X = function (a, b) {
                        var
                        c, d, f, g, h, j, k, o = "<td class='ui-pg-button " + n + "'><span class='ui-separator'></span></td>",
                            q = "",
                            s = "<table class='ui-pg-table ui-common-table ui-paging-pager'><tbody><tr>",
                            t = "",
                            u = function (a, b) {
                                var
                                c;
                                return "stop" !== (c = $(e).triggerHandler("jqGridPaging", [a, b])) && ($.isFunction(e.p.onPaging) && (c = e.p.onPaging.call(e, a, b)), "stop" !== c && (e.p.selrow = null, e.p.multiselect && (e.p.selarrrow = [], W(!1)), e.p.savedRow = [], !0))
                            };
                        if (a = a.substr(1), b += "_" + a, c = "pg_" + a, d = a + "_left", f = a + "_center", g = a + "_right", $("#" + $.jgrid.jqID(a)).append("<div id='" + c + "' class='ui-pager-control' role='group'><table " + l(m, "pagerTable", !1, "ui-pg-table ui-common-table ui-pager-table") + "><tbody><tr><td id='" + d + "' align='left'></td><td id='" + f + "' align='center' style='white-space:pre;'></td><td id='" + g + "' align='right'></td></tr></tbody></table></div>").attr("dir", "ltr"), e.p.rowList.length > 0) {
                            t = '<td dir="' + i + '">', t += "<select " + l(m, "pgSelectBox", !1, "ui-pg-selbox") + ' role="listbox" title="' + ($.jgrid.getRegional(e, "defaults.pgrecs", e.p.pgrecs) || "") + '">';
                            var
                            v;
                            for (k = 0; k < e.p.rowList.length; k++) v = e.p.rowList[k].toString().split(":"), 1 === v.length && (v[1] = v[0]), t += '<option role="option" value="' + v[0] + '"' + (A(e.p.rowNum, 0) === A(v[0], 0) ? ' selected="selected"' : "") + ">" + v[1] + "</option>";
                            t += "</select></td>"
                        }
                        if ("rtl" === i && (s += t), !0 === e.p.pginput && (q = "<td id='input" + b + "' dir='" + i + "'>" + $.jgrid.template($.jgrid.getRegional(e, "defaults.pgtext", e.p.pgtext) || "", "<input class='ui-pg-input' type='text' size='2' maxlength='7' value='0' role='textbox'/>", "<span id='sp_1_" + $.jgrid.jqID(a) + "'></span>") + "</td>"), !0 === e.p.pgbuttons) {
                            var
                            w = ["first" + b, "prev" + b, "next" + b, "last" + b],
                                x = l(m, "pgButtonBox", !0, "ui-pg-button"),
                                y = [$.jgrid.getRegional(e, "defaults.pgfirst", e.p.pgfirst) || "", $.jgrid.getRegional(e, "defaults.pgprev", e.p.pgprev) || "", $.jgrid.getRegional(e, "defaults.pgnext", e.p.pgnext) || "", $.jgrid.getRegional(e, "defaults.pglast", e.p.pglast) || ""];
                            "rtl" === i && (w.reverse(), y.reverse()), s += "<td id='" + w[0] + "' class='" + x + "' title='" + y[0] + "'><span " + l(m, "icon_first", !1, r) + "></span></td>", s += "<td id='" + w[1] + "' class='" + x + "'  title='" + y[1] + "'><span " + l(m, "icon_prev", !1, r) + "></span></td>", s += "" !== q ? o + q + o : "", s += "<td id='" + w[2] + "' class='" + x + "' title='" + y[2] + "'><span " + l(m, "icon_next", !1, r) + "></span></td>", s += "<td id='" + w[3] + "' class='" + x + "' title='" + y[3] + "'><span " + l(m, "icon_end", !1, r) + "></span></td>"
                        } else "" !== q && (s += q);
                        "ltr" === i && (s += t), s += "</tr></tbody></table>", !0 === e.p.viewrecords && $("td#" + a + "_" + e.p.recordpos, "#" + c).append("<div dir='" + i + "' style='text-align:" + e.p.recordpos + "' class='ui-paging-info'></div>"), $("td#" + a + "_" + e.p.pagerpos, "#" + c).append(s), j = $("#gbox_" + $.jgrid.jqID(e.p.id)).css("font-size") || "11px", $("#gbox_" + $.jgrid.jqID(e.p.id)).append("<div id='testpg' " + l(m, "entrieBox", !1, "ui-jqgrid") + " style='font-size:" + j + ";visibility:hidden;' ></div>"), h = $(s).clone().appendTo("#testpg").width(), $("#testpg").remove(), h > 0 && ("" !== q && (h += 50), $("td#" + a + "_" + e.p.pagerpos, "#" + c).width(h)), e.p._nvtd = [], e.p._nvtd[0] = h ? Math.floor((e.p.width - h) / 2) : Math.floor(e.p.width / 3), e.p._nvtd[1] = 0, s = null, $(".ui-pg-selbox", "#" + c).on("change", function () {
                            return !!u("records", this) && (e.p.page = Math.round(e.p.rowNum * (e.p.page - 1) / this.value - .5) + 1, e.p.rowNum = this.value, e.p.pager && $(".ui-pg-selbox", e.p.pager).val(this.value), e.p.toppager && $(".ui-pg-selbox", e.p.toppager).val(this.value), V(), !1)
                        }), !0 === e.p.pgbuttons && ($(".ui-pg-button", "#" + c).hover(function () {
                            $(this).hasClass(n) ? this.style.cursor = "default" : ($(this).addClass(p), this.style.cursor = "pointer")
                        }, function () {
                            $(this).hasClass(n) || ($(this).removeClass(p), this.style.cursor = "default")
                        }), $("#first" + $.jgrid.jqID(b) + ", #prev" + $.jgrid.jqID(b) + ", #next" + $.jgrid.jqID(b) + ", #last" + $.jgrid.jqID(b)).click(function () {
                            if ($(this).hasClass(n)) return !1;
                            var
                            a = A(e.p.page, 1),
                                c = A(e.p.lastpage, 1),
                                d = !1,
                                f = !0,
                                g = !0,
                                h = !0,
                                i = !0;
                            return 0 === c || 1 === c ? (f = !1, g = !1, h = !1, i = !1) : c > 1 && a >= 1 ? 1 === a ? (f = !1, g = !1) : a === c && (h = !1, i = !1) : c > 1 && 0 === a && (h = !1, i = !1, a = c - 1), !! u(this.id.split("_")[0], this) && (this.id === "first" + b && f && (e.p.page = 1, d = !0), this.id === "prev" + b && g && (e.p.page = a - 1, d = !0), this.id === "next" + b && h && (e.p.page = a + 1, d = !0), this.id === "last" + b && i && (e.p.page = c, d = !0), d && V(), !1)
                        })), !0 === e.p.pginput && $("#" + c).on("keypress", "input.ui-pg-input", function (a) {
                            return 13 === (a.charCode || a.keyCode || 0) ? !! u("user", this) && ($(this).val(A($(this).val(), 1)), e.p.page = $(this).val() > 0 ? $(this).val() : e.p.page, V(), !1) : this
                        })
                    }, Y = function (a, b, c) {
                        var
                        d, f = e.p.colModel,
                            g = e.p.frozenColumns ? b : e.grid.headers[a].el,
                            h = "";
                        $("span.ui-grid-ico-sort", g).addClass(n), $(g).attr("aria-selected", "false"), d = f[a].index || f[a].name, void
                        0 === c ? f[a].lso ? "asc" === f[a].lso ? (f[a].lso += "-desc", h = "desc") : "desc" === f[a].lso ? (f[a].lso += "-asc", h = "asc") : "asc-desc" !== f[a].lso && "desc-asc" !== f[a].lso || (f[a].lso = "") : f[a].lso = h = f[a].firstsortorder || "asc" : f[a].lso = h = c, h ? ($("span.s-ico", g).show(), $("span.ui-icon-" + h, g).removeClass(n), $(g).attr("aria-selected", "true")) : e.p.viewsortcols[0] || $("span.s-ico", g).hide();
                        var
                        i = u.indexOf(d); - 1 === i ? (u.push(d), v.push(h)) : h ? v[i] = h : (v.splice(i, 1), u.splice(i, 1)), e.p.sortorder = "", e.p.sortname = "";
                        for (var
                        j = 0, k = u.length; j < k; j++) j > 0 && (e.p.sortname += ", "), e.p.sortname += u[j], j !== k - 1 && (e.p.sortname += " " + v[j]);
                        e.p.sortorder = v[k - 1]
                    }, Z = function (a, b, c, d, f) {
                        if (e.p.colModel[b].sortable && !(e.p.savedRow.length > 0)) {
                            if (c || (e.p.lastsort === b && "" !== e.p.sortname ? "asc" === e.p.sortorder ? e.p.sortorder = "desc" : "desc" === e.p.sortorder && (e.p.sortorder = "asc") : e.p.sortorder = e.p.colModel[b].firstsortorder || "asc", e.p.page = 1), e.p.multiSort) Y(b, f, d);
                            else {
                                if (d) {
                                    if (e.p.lastsort === b && e.p.sortorder === d && !c) return;
                                    e.p.sortorder = d
                                }
                                var
                                g, h = e.grid.headers[e.p.lastsort] ? e.grid.headers[e.p.lastsort].el : null,
                                    i = e.p.frozenColumns ? f : e.grid.headers[b].el,
                                    j = "single" === e.p.viewsortcols[1];
                                g = $(h).find("span.ui-grid-ico-sort"), g.addClass(n), j && $(g).css("display", "none"), $(h).attr("aria-selected", "false"), e.p.frozenColumns && (g = e.grid.fhDiv.find("span.ui-grid-ico-sort"), g.addClass(n), j && g.css("display", "none"), e.grid.fhDiv.find("th").attr("aria-selected", "false")), g = $(i).find("span.ui-icon-" + e.p.sortorder), g.removeClass(n), j && g.css("display", ""), $(i).attr("aria-selected", "true"), e.p.viewsortcols[0] || (e.p.lastsort !== b ? (e.p.frozenColumns && e.grid.fhDiv.find("span.s-ico").hide(), $("span.s-ico", h).hide(), $("span.s-ico", i).show()) : "" === e.p.sortname && $("span.s-ico", i).show()), a = a.substring(5 + e.p.id.length + 1), e.p.sortname = e.p.colModel[b].index || a
                            }
                            if ("stop" === $(e).triggerHandler("jqGridSortCol", [e.p.sortname, b, e.p.sortorder])) return void(e.p.lastsort = b);
                            if ($.isFunction(e.p.onSortCol) && "stop" === e.p.onSortCol.call(e, e.p.sortname, b, e.p.sortorder)) return void(e.p.lastsort = b);
                            if ("local" === e.p.datatype ? e.p.deselectAfterSort && $(e).jqGrid("resetSelection") : (e.p.selrow = null, e.p.multiselect && W(!1), e.p.selarrrow = [], e.p.savedRow = []), e.p.scroll) {
                                var
                                k = e.grid.bDiv.scrollLeft;
                                J.call(e, !0, !1), e.grid.hDiv.scrollLeft = k
                            }
                            e.p.subGrid && "local" === e.p.datatype && $("td.sgexpanded", "#" + $.jgrid.jqID(e.p.id)).each(function () {
                                $(this).trigger("click")
                            }), e.p._sort = !0, V(), e.p.lastsort = b, e.p.sortname !== a && b && (e.p.lastsort = b)
                        }
                    }, _ = function () {
                        var
                        a, b, c, d, g = 0,
                            h = $.jgrid.cell_width ? 0 : A(e.p.cellLayout, 0),
                            i = 0,
                            j = A(e.p.scrollOffset, 0),
                            k = !1,
                            l = 0;
                        $.each(e.p.colModel, function () {
                            if (void
                            0 === this.hidden && (this.hidden = !1), e.p.grouping && e.p.autowidth) {
                                var
                                a = $.inArray(this.name, e.p.groupingView.groupField);
                                a >= 0 && e.p.groupingView.groupColumnShow.length > a && (this.hidden = !e.p.groupingView.groupColumnShow[a])
                            }
                            this.widthOrg = b = A(this.width, 0), !1 === this.hidden && (g += b + h, this.fixed ? l += b + h : i++)
                        }), isNaN(e.p.width) && (e.p.width = g + (!1 !== e.p.shrinkToFit || isNaN(e.p.height) ? 0 : j)), f.width = parseInt(e.p.width, 10), e.p.tblwidth = g, !1 === e.p.shrinkToFit && !0 === e.p.forceFit && (e.p.forceFit = !1), !0 === e.p.shrinkToFit && i > 0 && (c = f.width - h * i - l, isNaN(e.p.height) || (c -= j, k = !0), g = 0, $.each(e.p.colModel, function (d) {
                            !1 !== this.hidden || this.fixed || (b = Math.round(c * this.width / (e.p.tblwidth - h * i - l)), this.width = b, g += b, a = d)
                        }), d = 0, k ? f.width - l - (g + h * i) !== j && (d = f.width - l - (g + h * i) - j) : k || 1 === Math.abs(f.width - l - (g + h * i)) || (d = f.width - l - (g + h * i)), e.p.colModel[a].width += d, e.p.tblwidth = g + d + h * i + l, e.p.tblwidth > e.p.width && (e.p.colModel[a].width -= e.p.tblwidth - parseInt(e.p.width, 10), e.p.tblwidth = e.p.width))
                    }, aa = function (a) {
                        var
                        b, c = a,
                            d = a;
                        for (b = a + 1; b < e.p.colModel.length; b++) if (!0 !== e.p.colModel[b].hidden) {
                            d = b;
                            break
                        }
                        return d - c
                    }, ba = function (a) {
                        var
                        b = $(e.grid.headers[a].el),
                            c = [b.position().left + b.outerWidth()];
                        return "rtl" === e.p.direction && (c[0] = e.p.width - c[0]), c[0] -= e.grid.bDiv.scrollLeft, c.push($(e.grid.hDiv).position().top), c.push($(e.grid.bDiv).offset().top - $(e.grid.hDiv).offset().top + $(e.grid.bDiv).height()), c
                    }, ca = function (a) {
                        var
                        b, c = e.grid.headers,
                            d = $.jgrid.getCellIndex(a);
                        for (b = 0; b < c.length; b++) if (a === c[b].el) {
                            d = b;
                            break
                        }
                        return d
                    }, da = function (a, b, c) {
                        var
                        d, f, g = e.p.colModel,
                            h = g.length,
                            i = [],
                            j = $.jgrid.getRegional(e, "colmenu"),
                            k = '<ul id="col_menu" class="ui-search-menu  ui-col-menu modal-content" role="menu" tabindex="0" style="left:' + b + "px;top:" + a + 'px;">';
                        for (d = 0; d < h; d++) {
                            var
                            l = g[d].hidden ? "" : "checked",
                                m = g[d].name,
                                n = e.p.colNames[d];
                            f = "cb" === m || "subgrid" === m || "rn" === m || g[d].hidedlg ? "style='display:none'" : "", k += "<li " + f + ' class="ui-menu-item" role="presentation" draggable="true"><a class="g-menu-item" tabindex="0" role="menuitem" ><table class="ui-common-table" ><tr><td class="menu_icon" title="' + j.reorder + '"><span class="' + r + " " + s.icon_move + ' notclick"></span></td><td class="menu_icon"><input class="' + s.input_checkbox + '" type="checkbox" name="' + m + '" ' + l + '></td><td class="menu_text">' + n + "</td></tr></table></a></li>", i.push(d)
                        }
                        k += "</ul>", $(c).append(k), $("#col_menu").addClass("ui-menu " + s.menu_widget), $.fn.html5sortable() && $("#col_menu").html5sortable({
                            handle: "span",
                            forcePlaceholderSize: !0
                        }).on("sortupdate", function (a, b) {
                            for (i.splice(b.startindex, 1), i.splice(b.endindex, 0, b.startindex), $(e).jqGrid("destroyFrozenColumns"), $(e).jqGrid("remapColumns", i, !0), $(e).jqGrid("setFrozenColumns"), d = 0; d < h; d++) i[d] = d
                        }), $("#col_menu > li > a").on("click", function (a) {
                            var
                            b;
                            $(a.target).hasClass("notclick") || ($(a.target).is(":input") ? b = $(a.target).is(":checked") : (b = !$("input", this).is(":checked"), $("input", this).prop("checked", b)), b ? ($(e).jqGrid("showCol", $("input", this).attr("name")), $(this).parent().attr("draggable", "true")) : ($(e).jqGrid("hideCol", $("input", this).attr("name")), $(this).parent().attr("draggable", "false")))
                        }).hover(function () {
                            $(this).addClass(p)
                        }, function () {
                            $(this).removeClass(p)
                        })
                    }, ea = function (a, b, c, d) {
                        var
                        f, g, h, i, j, k = e.p.colModel[a],
                            l = "",
                            m = "",
                            n = "",
                            o = "",
                            q = "",
                            r = "",
                            t = ["eq", "ne", "lt", "le", "gt", "ge", "nu", "nn", "in", "ni"],
                            u = ["eq", "ne", "bw", "bn", "ew", "en", "cn", "nc", "nu", "nn", "in", "ni"],
                            v = $.jgrid.getRegional(e, "search"),
                            w = $.jgrid.styleUI[e.p.styleUI || "jQueryUI"].common;
                        if (k) {
                            f = !(!e.p.colFilters || !e.p.colFilters[k.name]) && e.p.colFilters[k.name], f && !$.isEmptyObject(f) && (l = f.oper1, m = f.value1, n = f.rule, o = f.oper2, q = f.value2), k.searchoptions || (k.searchoptions = {}), g = k.searchoptions.sopt ? k.searchoptions.sopt : "text" === k.sorttype ? u : t, h = k.searchoptions.groupOps ? k.searchoptions.groupOps : v.groupOps, j = $("<form></form>");
                            var
                            x = "<div>" + $.jgrid.getRegional(e, "colmenu.searchTitle") + "</div>";
                            x += '<div><select id="oper1" class="' + s.filter_select + '">', $.each(v.odata, function (a, b) {
                                i = b.oper === l ? 'selected="selected"' : "", -1 !== $.inArray(b.oper, g) && (r += '<option value="' + b.oper + '" ' + i + ">" + b.text + "</option>")
                            }), x += r, x += "</select></div>", j.append(x);
                            var
                            y = "";
                            k.searchoptions.defaultValue && (y = $.isFunction(k.searchoptions.defaultValue) ? k.searchoptions.defaultValue.call(e) : k.searchoptions.defaultValue), m && (y = m);
                            var
                            z = $.extend(k.searchoptions, {
                                name: k.index || k.name,
                                id: "sval1_" + e.p.idPrefix + k.name,
                                oper: "search"
                            }),
                                A = $.jgrid.createEl.call(e, k.stype, z, y, !1, $.extend({}, $.jgrid.ajaxOptions, e.p.ajaxSelectOptions || {}));
                            $(A).addClass(s.filter_input), x = $("<div></div>").append(A), j.append(x), x = '<div><select id="operand" class="' + s.filter_select + '">', $.each(h, function (a, b) {
                                i = b.op === n ? 'selected="selected"' : "", x += "<option value='" + b.op + "' " + i + ">" + b.text + "</option>"
                            }), x += "</select></div>", j.append(x), r = "", $.each(v.odata, function (a, b) {
                                i = b.oper === o ? 'selected="selected"' : "", -1 !== $.inArray(b.oper, g) && (r += '<option value="' + b.oper + '" ' + i + ">" + b.text + "</option>")
                            }), x = '<div><select id="oper2" class="' + s.filter_select + '">' + r + "</select></div>", j.append(x), y = q || "", z = $.extend(k.searchoptions, {
                                name: k.index || k.name,
                                id: "sval2_" + e.p.idPrefix + k.name,
                                oper: "search"
                            }), A = $.jgrid.createEl.call(e, k.stype, z, y, !1, $.extend({}, $.jgrid.ajaxOptions, e.p.ajaxSelectOptions || {})), $(A).addClass(s.filter_input), x = $("<div></div>").append(A), j.append(x), x = "<div>", x += "<div class='search_buttons'><a tabindex='0' id='bs_reset' class='fm-button " + w.button + " ui-reset'>" + v.Reset + "</a></div>", x += "<div class='search_buttons'><a tabindex='0' id='bs_search' class='fm-button " + w.button + " ui-search'>" + v.Find + "</a></div>", x += "</div>", j.append(x), j = $('<li class="ui-menu-item" role="presentation"></li>').append(j), j = $('<ul id="search_menu" class="ui-search-menu modal-content" role="menu" tabindex="0" style="left:' + c + "px;top:" + b + 'px;"></ul>').append(j), $(d).append(j), $("#search_menu").addClass("ui-menu " + s.menu_widget), $("#bs_reset, #bs_search", "#search_menu").hover(function () {
                                $(this).addClass(p)
                            }, function () {
                                $(this).removeClass(p)
                            }), $("#bs_reset", j).on("click", function (a) {
                                e.p.colFilters[k.name] = {}, e.p.postData.filters = fa(), e.p.search = !1, $(e).trigger("reloadGrid"), $("#column_menu").remove()
                            }), $("#bs_search", j).on("click", function (a) {
                                e.p.colFilters[k.name] = {
                                    oper1: $("#oper1", "#search_menu").val(),
                                    value1: $("#sval1_" + e.p.idPrefix + k.name, "#search_menu").val(),
                                    rule: $("#operand", "#search_menu").val(),
                                    oper2: $("#oper2", "#search_menu").val(),
                                    value2: $("#sval2_" + e.p.idPrefix + k.name, "#search_menu").val()
                                }, e.p.postData.filters = fa(), e.p.search = !0, $(e).trigger("reloadGrid"), $("#column_menu").remove()
                            })
                        }
                    }, fa = function () {
                        var
                        a = "AND",
                            b = '{"groupOp":"' + a + '","rules":[], "groups" : [',
                            c = 0;
                        for (var
                        d in e.p.colFilters) if (e.p.colFilters.hasOwnProperty(d)) {
                            var
                            f = e.p.colFilters[d];
                            $.isEmptyObject(f) || (c > 0 && (b += ","), b += '{"groupOp": "' + f.rule + '", "rules" : [', b += '{"field":"' + d + '",', b += '"op":"' + f.oper1 + '",', f.value1 += "", b += '"data":"' + f.value1.replace(/\\/g, "\\\\").replace(/\"/g, '\\"') + '"}', f.value2 && (b += ',{"field":"' + d + '",', b += '"op":"' + f.oper2 + '",', f.value2 += "", b += '"data":"' + f.value2.replace(/\\/g, "\\\\").replace(/\"/g, '\\"') + '"}'), b += "]}", c++)
                        }
                        return b += "]}"
                    }, ga = function (a, b) {
                        var
                        c = e.p.colModel[a],
                            d = e.p.groupingView; - 1 !== b ? d.groupField.splice(b, 1) : d.groupField.push(c.name), $(e).jqGrid("groupingGroupBy", d.groupField), e.p.frozenColumns && ($(e).jqGrid("destroyFrozenColumns"), $(e).jqGrid("setFrozenColumns"))
                    }, ha = function (a, b) {
                        var
                        c, d = [],
                            f = e.p.colModel.length,
                            g = -1,
                            h = e.p.colModel;
                        for (c = 0; c < f; c++) h[c].frozen && (g = c), d.push(c);
                        d.splice(a, 1), d.splice(g + (b ? 1 : 0), 0, a), h[a].frozen = b, $(e).jqGrid("destroyFrozenColumns"), $(e).jqGrid("remapColumns", d, !0), $(e).jqGrid("setFrozenColumns")
                    }, ia = function (a, b, c) {
                        b = parseInt(b, 10), c = parseInt(c, 10) + 25;
                        var
                        d, f, g = $(".ui-jqgrid-view").css("font-size") || "11px",
                            h = '<ul id="column_menu" class="ui-search-menu modal-content column-menu" role="menu" tabindex="0" style="font-size:' + g + ";left:" + b + "px;top:" + c + 'px;">',
                            i = e.p.colModel[a],
                            j = $.extend({
                                sorting: !0,
                                columns: !0,
                                filtering: !0,
                                seraching: !0,
                                grouping: !0,
                                freeze: !0
                            }, i.coloptions),
                            k = $.jgrid.getRegional(e, "colmenu"),
                            l = e.p.colNames[a];
                        if (j.sorting && (h += '<li class="ui-menu-item" role="presentation"><a class="g-menu-item" tabindex="0" role="menuitem" value="sortasc"><table class="ui-common-table"><tr><td class="menu_icon"><span class="' + r + " " + s.icon_sort_asc + '"></span></td><td class="menu_text">' + k.sortasc + "</td></tr></table></a></li>", h += '<li class="ui-menu-item" role="presentation"><a class="g-menu-item" tabindex="0" role="menuitem" value="sortdesc"><table class="ui-common-table"><tr><td class="menu_icon"><span class="' + r + " " + s.icon_sort_desc + '"></span></td><td class="menu_text">' + k.sortdesc + "</td></tr></table></a></li>"), j.columns && (h += '<li class="ui-menu-item divider" role="separator"></li>', h += '<li class="ui-menu-item" role="presentation"><a class="g-menu-item" tabindex="0" role="menuitem" value="columns"><table class="ui-common-table"><tr><td class="menu_icon"><span class="' + r + " " + s.icon_columns + '"></span></td><td class="menu_text">' + k.columns + "</td></tr></table></a></li>"), j.filtering && (h += '<li class="ui-menu-item divider" role="separator"></li>', h += '<li class="ui-menu-item" role="presentation"><a class="g-menu-item" tabindex="0" role="menuitem" value="filtering"><table class="ui-common-table"><tr><td class="menu_icon"><span class="' + r + " " + s.icon_filter + '"></span></td><td class="menu_text">' + k.filter + " " + l + "</td></tr></table></a></li>"), j.grouping && (d = $.inArray(i.name, e.p.groupingView.groupField), h += '<li class="ui-menu-item divider" role="separator"></li>', h += '<li class="ui-menu-item" role="presentation"><a class="g-menu-item" tabindex="0" role="menuitem" value="grouping"><table class="ui-common-table"><tr><td class="menu_icon"><span class="' + r + " " + s.icon_group + '"></span></td><td class="menu_text">' + (-1 !== d ? k.ungrouping : k.grouping + " " + l) + "</td></tr></table></a></li>"), j.freeze && (f = !i.frozen || !e.p.frozenColumns, h += '<li class="ui-menu-item divider" role="separator"></li>', h += '<li class="ui-menu-item" role="presentation"><a class="g-menu-item" tabindex="0" role="menuitem" value="freeze"><table class="ui-common-table"><tr><td class="menu_icon"><span class="' + r + " " + s.icon_freeze + '"></span></td><td class="menu_text">' + (f ? k.freeze + " " + l : k.unfreeze) + "</td></tr></table></a></li>"), h += "</ul>", $("body").append(h), $("#column_menu").addClass("ui-menu " + s.menu_widget), "ltr" === e.p.direction) {
                            var
                            m = $("#column_menu").width() + 26;
                            $("#column_menu").css("left", b - m + "px")
                        }
                        $("#column_menu > li > a").hover(function () {
                            $("#col_menu").remove(), $("#search_menu").remove();
                            var
                            b, c;
                            "columns" === $(this).attr("value") && (b = $(this).parent().width() + 18, c = $(this).parent().position().top - 5, da(c, b, $(this).parent())), "filtering" === $(this).attr("value") && (b = $(this).parent().width() + 18, c = $(this).parent().position().top - 5, ea(a, c, b, $(this).parent())), $(this).addClass(p)
                        }, function () {
                            $(this).removeClass(p)
                        }).click(function () {
                            var
                            b = $(this).attr("value"),
                                c = e.grid.headers[a].el;
                            "sortasc" === b ? Z("jqgh_" + e.p.id + "_" + i.name, a, !0, "asc", c) : "sortdesc" === b ? Z("jqgh_" + e.p.id + "_" + i.name, a, !0, "desc", c) : "grouping" === b ? ga(a, d) : "freeze" === b && ha(a, f), -1 === b.indexOf("sort") && "grouping" !== b && "freeze" !== b || $(this).remove()
                        })
                    };
                for (e.p.colMenu && $("body").on("click", function (a) {
                    $(a.target).closest(".column-menu").length || $("#column_menu").remove()
                }), this.p.id = this.id, -1 === $.inArray(e.p.multikey, z) && (e.p.multikey = !1), e.p.keyName = !1, j = 0; j < e.p.colModel.length; j++) y = "string" == typeof
                e.p.colModel[j].template ? null != $.jgrid.cmTemplate && "object" == typeof
                $.jgrid.cmTemplate[e.p.colModel[j].template] ? $.jgrid.cmTemplate[e.p.colModel[j].template] : {} : e.p.colModel[j].template, e.p.colModel[j] = $.extend(!0, {}, e.p.cmTemplate, y || {}, e.p.colModel[j]), !1 === e.p.keyName && !0 === e.p.colModel[j].key && (e.p.keyName = e.p.colModel[j].name, e.p.keyIndex = j);
                if (e.p.sortorder = e.p.sortorder.toLowerCase(), $.jgrid.cell_width = $.jgrid.cellWidth(), !0 === e.p.grouping && (e.p.scroll = !1, e.p.rownumbers = !1, e.p.treeGrid = !1, e.p.gridview = !0), !0 === this.p.treeGrid) {
                    try {
                        $(this).jqGrid("setTreeGrid")
                    } catch (a) {}
                    "local" !== e.p.datatype && (e.p.localReader = {
                        id: "_id_"
                    })
                }
                if (this.p.subGrid) try {
                    $(e).jqGrid("setSubGrid")
                } catch (a) {}
                this.p.multiselect && (this.p.colNames.unshift("<input role='checkbox' id='cb_" + this.p.id + "' class='cbox' type='checkbox'/>"), this.p.colModel.unshift({
                    name: "cb",
                    width: $.jgrid.cell_width ? e.p.multiselectWidth + e.p.cellLayout : e.p.multiselectWidth,
                    sortable: !1,
                    resizable: !1,
                    hidedlg: !0,
                    search: !1,
                    align: "center",
                    fixed: !0,
                    frozen: !0
                })), this.p.rownumbers && (this.p.colNames.unshift(""), this.p.colModel.unshift({
                    name: "rn",
                    width: e.p.rownumWidth,
                    sortable: !1,
                    resizable: !1,
                    hidedlg: !0,
                    search: !1,
                    align: "center",
                    fixed: !0,
                    frozen: !0
                })), e.p.xmlReader = $.extend(!0, {
                    root: "rows",
                    row: "row",
                    page: "rows>page",
                    total: "rows>total",
                    records: "rows>records",
                    repeatitems: !0,
                    cell: "cell",
                    id: "[id]",
                    userdata: "userdata",
                    subgrid: {
                        root: "rows",
                        row: "row",
                        repeatitems: !0,
                        cell: "cell"
                    }
                }, e.p.xmlReader), e.p.jsonReader = $.extend(!0, {
                    root: "rows",
                    page: "page",
                    total: "total",
                    records: "records",
                    repeatitems: !0,
                    cell: "cell",
                    id: "id",
                    userdata: "userdata",
                    subgrid: {
                        root: "rows",
                        repeatitems: !0,
                        cell: "cell"
                    }
                }, e.p.jsonReader), e.p.localReader = $.extend(!0, {
                    root: "rows",
                    page: "page",
                    total: "total",
                    records: "records",
                    repeatitems: !1,
                    cell: "cell",
                    id: "id",
                    userdata: "userdata",
                    subgrid: {
                        root: "rows",
                        repeatitems: !0,
                        cell: "cell"
                    }
                }, e.p.localReader), e.p.scroll && (e.p.pgbuttons = !1, e.p.pginput = !1, e.p.rowList = []), e.p.data.length && (K(), L());
                var
                ja, ka, la, ma, na, oa, pa, qa, ra, sa = "<thead><tr class='ui-jqgrid-labels' role='row'>",
                    ta = "",
                    ua = "",
                    va = "";
                if (!0 === e.p.shrinkToFit && !0 === e.p.forceFit) for (j = e.p.colModel.length - 1; j >= 0; j--) if (!e.p.colModel[j].hidden) {
                    e.p.colModel[j].resizable = !1;
                    break
                }
                if ("horizontal" === e.p.viewsortcols[1] ? (ua = " ui-i-asc", va = " ui-i-desc") : "single" === e.p.viewsortcols[1] && (ua = " ui-single-sort-asc", va = " ui-single-sort-desc", ta = " style='display:none'", e.p.viewsortcols[0] = !1), ja = t ? "class='ui-th-div-ie'" : "", qa = "<span class='s-ico' style='display:none'>", qa += "<span sort='asc'  class='ui-grid-ico-sort ui-icon-asc" + ua + " ui-sort-" + i + " " + n + " " + r + " " + l(m, "icon_asc", !0) + "'" + ta + "></span>", qa += "<span sort='desc' class='ui-grid-ico-sort ui-icon-desc" + va + " ui-sort-" + i + " " + n + " " + r + " " + l(m, "icon_desc", !0) + "'" + ta + "></span></span>", e.p.multiSort && e.p.sortname) for (u = e.p.sortname.split(","), j = 0; j < u.length; j++) w = $.trim(u[j]).split(" "), u[j] = $.trim(w[0]), v[j] = w[1] ? $.trim(w[1]) : e.p.sortorder || "asc";
                for (j = 0; j < this.p.colNames.length; j++) {
                    var
                    wa = e.p.headertitles ? ' title="' + $.jgrid.stripHtml(e.p.colNames[j]) + '"' : "";
                    ra = e.p.colModel[j], ra.hasOwnProperty("colmenu") || (ra.colmenu = "rn" !== ra.name && "cb" !== ra.name && "subgrid" !== ra.name), sa += "<th id='" + e.p.id + "_" + ra.name + "' role='columnheader' " + l(m, "headerBox", !1, "ui-th-column ui-th-" + i) + " " + wa + ">", ka = ra.index || ra.name, sa += "<div class='ui-th-div' id='jqgh_" + e.p.id + "_" + ra.name + "' " + ja + ">" + e.p.colNames[j], ra.width ? ra.width = parseInt(ra.width, 10) : ra.width = 150, "boolean" != typeof
                    ra.title && (ra.title = !0), ra.lso = "", ka === e.p.sortname && (e.p.lastsort = j), e.p.multiSort && -1 !== (w = $.inArray(ka, u)) && (ra.lso = v[w]), sa += qa, e.p.colMenu && ra.colmenu && (sa += "<a class='colmenu' href='#/'><span class='colmenuspan " + r + " " + s.icon_menu + "'></span></a>"), sa += "</div></th>"
                }
                if (sa += "</tr></thead>", qa = null, ra = null, $(this).append(sa), $("thead tr:first th", this).hover(function () {
                    $(this).addClass(p)
                }, function () {
                    $(this).removeClass(p)
                }), this.p.multiselect) {
                    var
                    xa, ya = [];
                    $("#cb_" + $.jgrid.jqID(e.p.id), this).on("click", function () {
                        e.p.selarrrow = [];
                        var
                        a = !0 === e.p.frozenColumns ? e.p.id + "_frozen" : "";
                        this.checked ? ($(e.rows).each(function (b) {
                            b > 0 && ($(this).hasClass("ui-subgrid") || $(this).hasClass("jqgroup") || $(this).hasClass(n) || $(this).hasClass("jqfoot") || ($("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + $.jgrid.jqID(this.id))[e.p.useProp ? "prop" : "attr"]("checked", !0), $(this).addClass(o).attr("aria-selected", "true"), e.p.selarrrow.push(this.id), e.p.selrow = this.id, a && ($("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + $.jgrid.jqID(this.id), e.grid.fbDiv)[e.p.useProp ? "prop" : "attr"]("checked", !0), $("#" + $.jgrid.jqID(this.id), e.grid.fbDiv).addClass(o))))
                        }), xa = !0, ya = []) : ($(e.rows).each(function (b) {
                            b > 0 && ($(this).hasClass("ui-subgrid") || $(this).hasClass("jqgroup") || $(this).hasClass(n) || $(this).hasClass("jqfoot") || ($("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + $.jgrid.jqID(this.id))[e.p.useProp ? "prop" : "attr"]("checked", !1), $(this).removeClass(o).attr("aria-selected", "false"), ya.push(this.id), a && ($("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + $.jgrid.jqID(this.id), e.grid.fbDiv)[e.p.useProp ? "prop" : "attr"]("checked", !1), $("#" + $.jgrid.jqID(this.id), e.grid.fbDiv).removeClass(o))))
                        }), e.p.selrow = null, xa = !1), $(e).triggerHandler("jqGridSelectAll", [xa ? e.p.selarrrow : ya, xa]), $.isFunction(e.p.onSelectAll) && e.p.onSelectAll.call(e, xa ? e.p.selarrrow : ya, xa)
                    })
                }
                if (!0 === e.p.autowidth) {
                    var
                    za = $(x).innerWidth();
                    e.p.width = za > 0 ? za : "nw"
                }
                _(), $(x).css("width", f.width + "px").append("<div class='ui-jqgrid-resize-mark' id='rs_m" + e.p.id + "'>&#160;</div>"), e.p.scrollPopUp && $(x).append("<div " + l(m, "scrollBox", !1, "loading ui-scroll-popup") + " id='scroll_g" + e.p.id + "'></div>"), $(k).css("width", f.width + "px"), sa = $("thead:first", e).get(0);
                var
                Aa = "";
                e.p.footerrow && (Aa += "<table role='presentation' style='width:" + e.p.tblwidth + "px' " + l(m, "footerTable", !1, "ui-jqgrid-ftable ui-common-table") + "><tbody><tr role='row' " + l(m, "footerBox", !1, "footrow footrow-" + i) + ">");
                var
                Ba = $("tr:first", sa),
                    Ca = "<tr class='jqgfirstrow' role='row'>";
                if (e.p.disableClick = !1, $("th", Ba).each(function (a) {
                    ra = e.p.colModel[a], la = ra.width, void
                    0 === ra.resizable && (ra.resizable = !0), ra.resizable ? (ma = document.createElement("span"), $(ma).html("&#160;").addClass("ui-jqgrid-resize ui-jqgrid-resize-" + i).css("cursor", "col-resize"), $(this).addClass(e.p.resizeclass)) : ma = "", $(this).css("width", la + "px").prepend(ma), ma = null;
                    var
                    b = "";
                    ra.hidden && ($(this).css("display", "none"), b = "display:none;"), Ca += "<td role='gridcell' style='height:0px;width:" + la + "px;" + b + "'></td>", f.headers[a] = {
                        width: la,
                        el: this
                    }, "boolean" != typeof (ta = ra.sortable) && (ra.sortable = !0, ta = !0);
                    var
                    c = ra.name;
                    "cb" !== c && "subgrid" !== c && "rn" !== c && e.p.viewsortcols[2] && $(">div", this).addClass("ui-jqgrid-sortable"), ta && (e.p.multiSort ? e.p.viewsortcols[0] ? ($("div span.s-ico", this).show(), e.tmpcm.lso && $("div span.ui-icon-" + ra.lso, this).removeClass(n).css("display", "")) : ra.lso && ($("div span.s-ico", this).show(), $("div span.ui-icon-" + ra.lso, this).removeClass(n).css("display", "")) : e.p.viewsortcols[0] ? ($("div span.s-ico", this).show(), a === e.p.lastsort && $("div span.ui-icon-" + e.p.sortorder, this).removeClass(n).css("display", "")) : a === e.p.lastsort && "" !== e.p.sortname && ($("div span.s-ico", this).show(), $("div span.ui-icon-" + e.p.sortorder, this).removeClass(n).css("display", ""))), e.p.footerrow && (Aa += "<td role='gridcell' " + B(a, 0, "", null, "", !1) + ">&#160;</td>")
                }).mousedown(function (a) {
                    if (1 === $(a.target).closest("th>span.ui-jqgrid-resize").length) {
                        var
                        b = ca(this);
                        return !0 === e.p.forceFit && (e.p.nv = aa(b)), f.dragStart(b, a, ba(b)), !1
                    }
                }).click(function (a) {
                    if (e.p.disableClick) return e.p.disableClick = !1, !1;
                    var
                    b, c, d = "th>div.ui-jqgrid-sortable";
                    e.p.viewsortcols[2] || (d = "th>div>span>span.ui-grid-ico-sort");
                    var
                    f = $(a.target).closest(d);
                    if (1 === f.length) {
                        var
                        g;
                        if (e.p.frozenColumns) {
                            var
                            h = $(this)[0].id.substring(e.p.id.length + 1);
                            $(e.p.colModel).each(function (a) {
                                if (this.name === h) return g = a, !1
                            })
                        } else g = ca(this);
                        if ($(a.target).hasClass("colmenuspan")) {
                            null != $("#column_menu")[0] && $("#column_menu").remove();
                            var
                            i = $.jgrid.getCellIndex(a.target);
                            if (-1 === i) return;
                            var
                            j = $(this).offset(),
                                k = j.left,
                                l = j.top;
                            return "ltr" === e.p.direction && (k += $(this).outerWidth()), ia(i, k, l, f), void
                            a.stopPropagation()
                        }
                        return e.p.viewsortcols[2] || (b = !0, c = f.attr("sort")), null != g && Z($("div", this)[0].id, g, b, c, this), !1
                    }
                }), ra = null, e.p.sortable && $.fn.sortable) try {
                    $(e).jqGrid("sortableColumns", Ba)
                } catch (a) {}
                e.p.footerrow && (Aa += "</tr></tbody></table>"), Ca += "</tr>", pa = document.createElement("tbody"), this.appendChild(pa), $(this).addClass(l(m, "rowTable", !0, "ui-jqgrid-btable ui-common-table")).append(Ca), e.p.altRows && $(this).addClass(l(m, "stripedTable", !0, "")), Ca = null;
                var
                Da = $("<table " + l(m, "headerTable", !1, "ui-jqgrid-htable ui-common-table") + " style='width:" + e.p.tblwidth + "px' role='presentation' aria-labelledby='gbox_" + this.id + "'></table>").append(sa),
                    Ea = !(!e.p.caption || !0 !== e.p.hiddengrid),
                    Fa = $("<div class='ui-jqgrid-hbox" + ("rtl" === i ? "-rtl" : "") + "'></div>"),
                    Ga = "Bootstrap" !== e.p.styleUI || isNaN(e.p.height) ? 0 : 2;
                sa = null, f.hDiv = document.createElement("div"), f.hDiv.style.width = f.width - Ga + "px", f.hDiv.className = l(m, "headerDiv", !0, "ui-jqgrid-hdiv"), $(f.hDiv).append(Fa), $(Fa).append(Da), Da = null, Ea && $(f.hDiv).hide(), e.p.pager && ("string" == typeof
                e.p.pager ? "#" !== e.p.pager.substr(0, 1) && (e.p.pager = "#" + e.p.pager) : e.p.pager = "#" + $(e.p.pager).attr("id"), $(e.p.pager).css({
                    width: f.width + "px"
                }).addClass(l(m, "pagerBox", !0, "ui-jqgrid-pager")).appendTo(x), Ea && $(e.p.pager).hide(), X(e.p.pager, "")), !1 === e.p.cellEdit && !0 === e.p.hoverrows && $(e).on({
                    mouseover: function (a) {
                        oa = $(a.target).closest("tr.jqgrow"), "ui-subgrid" !== $(oa).attr("class") && $(oa).addClass(p)
                    },
                    mouseout: function (a) {
                        oa = $(a.target).closest("tr.jqgrow"), $(oa).removeClass(p)
                    }
                });
                var
                Ha, Ia, Ja;
                $(e).before(f.hDiv).on({
                    click: function (a) {
                        if (na = a.target, oa = $(na, e.rows).closest("tr.jqgrow"), 0 === $(oa).length || oa[0].className.indexOf(n) > -1 || ($(na, e).closest("table.ui-jqgrid-btable").attr("id") || "").replace("_frozen", "") !== e.id) return this;
                        var
                        c = $(na).filter(":enabled").hasClass("cbox"),
                            d = $(e).triggerHandler("jqGridBeforeSelectRow", [oa[0].id, a]);
                        if (d = !1 !== d && "stop" !== d, $.isFunction(e.p.beforeSelectRow)) {
                            var
                            f = e.p.beforeSelectRow.call(e, oa[0].id, a);
                            !1 !== f && "stop" !== f || (d = !1)
                        }
                        if ("A" !== na.tagName && ("INPUT" !== na.tagName && "TEXTAREA" !== na.tagName && "OPTION" !== na.tagName && "SELECT" !== na.tagName || c)) if (Ha = oa[0].id, na = $(na).closest("tr.jqgrow>td"), na.length > 0 && (Ia = $.jgrid.getCellIndex(na)), !0 !== e.p.cellEdit) {
                            if (na.length > 0 && (Ja = $(na).closest("td,th").html(), $(e).triggerHandler("jqGridCellSelect", [Ha, Ia, Ja, a]), $.isFunction(e.p.onCellSelect) && e.p.onCellSelect.call(e, Ha, Ia, Ja, a)), d) if (e.p.multimail && e.p.multiselect) {
                                if (a.shiftKey) {
                                    if (c) {
                                        var
                                        g = $(e).jqGrid("getGridParam", "selrow"),
                                            h = $(e).jqGrid("getInd", Ha),
                                            i = $(e).jqGrid("getInd", g),
                                            j = "",
                                            k = "";
                                        h > i ? (j = g, k = Ha) : (j = Ha, k = g);
                                        var
                                        l = !1,
                                            m = !1,
                                            o = !0;
                                        return $.inArray(Ha, e.p.selarrrow) > -1 && (o = !1), $.each($(this).getDataIDs(), function (a, b) {
                                            return (m = b === j || m) && $(e).jqGrid("resetSelection", b), b !== k
                                        }), o && $.each($(this).getDataIDs(), function (a, b) {
                                            return (l = b === j || l) && $(e).jqGrid("setSelection", b, !1), b !== k
                                        }), void(e.p.selrow = h > i ? k : j)
                                    }
                                    window.getSelection().removeAllRanges()
                                }
                                b(Ha, c, a, !1)
                            } else e.p.multikey ? a[e.p.multikey] ? $(e).jqGrid("setSelection", Ha, !0, a) : e.p.multiselect && c && (c = $("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + Ha).is(":checked"), $("#jqg_" + $.jgrid.jqID(e.p.id) + "_" + Ha)[e.p.useProp ? "prop" : "attr"]("checked", !c)) : b(Ha, c, a, !0)
                        } else if (e.p.multiselect && c && d) $(e).jqGrid("setSelection", Ha, !0, a);
                        else if (na.length > 0) try {
                            $(e).jqGrid("editCell", oa[0].rowIndex, Ia, !0)
                        } catch (a) {}
                    },
                    reloadGrid: function (a, b) {
                        if (!0 === e.p.treeGrid && (e.p.datatype = e.p.treedatatype), b = b || {}, b.current && e.grid.selectionPreserver(e), "local" === e.p.datatype ? ($(e).jqGrid("resetSelection"), e.p.data.length && (K(), L())) : e.p.treeGrid || (e.p.selrow = null, e.p.multiselect && (e.p.selarrrow = [], W(!1)), e.p.savedRow = []), e.p.scroll && J.call(e, !0, !1), b.page) {
                            var
                            c = b.page;
                            c > e.p.lastpage && (c = e.p.lastpage), c < 1 && (c = 1), e.p.page = c, e.grid.prevRowHeight ? e.grid.bDiv.scrollTop = (c - 1) * e.grid.prevRowHeight * e.p.rowNum : e.grid.bDiv.scrollTop = 0
                        }
                        return e.grid.prevRowHeight && e.p.scroll && void
                        0 === b.page ? (delete
                        e.p.lastpage, e.grid.populateVisible()) : e.grid.populate(), !0 === e.p.inlineNav && $(e).jqGrid("showAddEditButtons"), !1
                    },
                    dblclick: function (a) {
                        if (na = a.target, oa = $(na, e.rows).closest("tr.jqgrow"), 0 !== $(oa).length) {
                            Ha = oa[0].rowIndex, Ia = $.jgrid.getCellIndex(na);
                            var
                            b = $(e).triggerHandler("jqGridDblClickRow", [$(oa).attr("id"), Ha, Ia, a]);
                            return null != b ? b : $.isFunction(e.p.ondblClickRow) && null != (b = e.p.ondblClickRow.call(e, $(oa).attr("id"), Ha, Ia, a)) ? b : void
                            0
                        }
                    },
                    contextmenu: function (a) {
                        if (na = a.target, oa = $(na, e.rows).closest("tr.jqgrow"), 0 !== $(oa).length) {
                            e.p.multiselect || $(e).jqGrid("setSelection", oa[0].id, !0, a), Ha = oa[0].rowIndex, Ia = $.jgrid.getCellIndex(na);
                            var
                            b = $(e).triggerHandler("jqGridRightClickRow", [$(oa).attr("id"), Ha, Ia, a]);
                            return null != b ? b : $.isFunction(e.p.onRightClickRow) && null != (b = e.p.onRightClickRow.call(e, $(oa).attr("id"), Ha, Ia, a)) ? b : void
                            0
                        }
                    }
                }), f.bDiv = document.createElement("div"), t && "auto" === String(e.p.height).toLowerCase() && (e.p.height = "100%"), $(f.bDiv).append($('<div style="position:relative;"></div>').append("<div></div>").append(this)).addClass("ui-jqgrid-bdiv").css({
                    height: e.p.height + (isNaN(e.p.height) ? "" : "px"),
                    width: f.width - Ga + "px"
                }).scroll(f.scrollGrid), $("table:first", f.bDiv).css({
                    width: e.p.tblwidth + "px"
                }), $.support.tbody || 2 === $("tbody", this).length && $("tbody:gt(0)", this).remove(), e.p.multikey && ($.jgrid.msie() ? $(f.bDiv).on("selectstart", function () {
                    return !1
                }) : $(f.bDiv).on("mousedown", function () {
                    return !1
                })), Ea && $(f.bDiv).hide();
                var
                Ka = r + " " + l(m, "icon_caption_open", !0),
                    La = r + " " + l(m, "icon_caption_close", !0);
                f.cDiv = document.createElement("div");
                var
                Ma = !0 === e.p.hidegrid ? $("<a role='link' class='ui-jqgrid-titlebar-close HeaderButton " + q + "' title='" + ($.jgrid.getRegional(e, "defaults.showhide", e.p.showhide) || "") + "' />").hover(function () {
                    Ma.addClass(p)
                }, function () {
                    Ma.removeClass(p)
                }).append("<span class='ui-jqgrid-headlink " + Ka + "'></span>").css("rtl" === i ? "left" : "right", "0px") : "";
                if ($(f.cDiv).append(Ma).append("<span class='ui-jqgrid-title'>" + e.p.caption + "</span>").addClass("ui-jqgrid-titlebar ui-jqgrid-caption" + ("rtl" === i ? "-rtl" : "") + " " + l(m, "gridtitleBox", !0)), $(f.cDiv).insertBefore(f.hDiv), e.p.toolbar[0]) {
                    var
                    Na = l(m, "customtoolbarBox", !0, "ui-userdata");
                    f.uDiv = document.createElement("div"), "top" === e.p.toolbar[1] ? $(f.uDiv).insertBefore(f.hDiv) : "bottom" === e.p.toolbar[1] && $(f.uDiv).insertAfter(f.hDiv), "both" === e.p.toolbar[1] ? (f.ubDiv = document.createElement("div"), $(f.uDiv).addClass(Na + " ui-userdata-top").attr("id", "t_" + this.id).insertBefore(f.hDiv).width(f.width - Ga), $(f.ubDiv).addClass(Na + " ui-userdata-bottom").attr("id", "tb_" + this.id).insertAfter(f.hDiv).width(f.width - Ga), Ea && $(f.ubDiv).hide()) : $(f.uDiv).width(f.width - Ga).addClass(Na + " ui-userdata-top").attr("id", "t_" + this.id), Ea && $(f.uDiv).hide()
                }
                if (e.p.toppager && (e.p.toppager = $.jgrid.jqID(e.p.id) + "_toppager", f.topDiv = $("<div id='" + e.p.toppager + "'></div>")[0], e.p.toppager = "#" + e.p.toppager, $(f.topDiv).addClass(l(m, "toppagerBox", !0, "ui-jqgrid-toppager")).width(f.width - Ga).insertBefore(f.hDiv), X(e.p.toppager, "_t")), e.p.footerrow && (f.sDiv = $("<div class='ui-jqgrid-sdiv'></div>")[0], Fa = $("<div class='ui-jqgrid-hbox" + ("rtl" === i ? "-rtl" : "") + "'></div>"), $(f.sDiv).append(Fa).width(f.width - Ga).insertAfter(f.hDiv), $(Fa).append(Aa), f.footers = $(".ui-jqgrid-ftable", f.sDiv)[0].rows[0].cells, e.p.rownumbers && (f.footers[0].className = l(m, "rownumBox", !0, "jqgrid-rownum")), Ea && $(f.sDiv).hide()), Fa = null, e.p.caption) {
                    var
                    Oa = e.p.datatype;
                    !0 === e.p.hidegrid && ($(".ui-jqgrid-titlebar-close", f.cDiv).click(function (a) {
                        var
                        b, c = $.isFunction(e.p.onHeaderClick),
                            d = ".ui-jqgrid-bdiv, .ui-jqgrid-hdiv, .ui-jqgrid-toppager, .ui-jqgrid-pager, .ui-jqgrid-sdiv",
                            g = this;
                        return !0 === e.p.toolbar[0] && ("both" === e.p.toolbar[1] && (d += ", #" + $(f.ubDiv).attr("id")), d += ", #" + $(f.uDiv).attr("id")), b = $(d, "#gview_" + $.jgrid.jqID(e.p.id)).length, "visible" === e.p.gridstate ? $(d, "#gbox_" + $.jgrid.jqID(e.p.id)).slideUp("fast", function () {
                            0 === --b && ($("span", g).removeClass(Ka).addClass(La), e.p.gridstate = "hidden", $("#gbox_" + $.jgrid.jqID(e.p.id)).hasClass("ui-resizable") && $(".ui-resizable-handle", "#gbox_" + $.jgrid.jqID(e.p.id)).hide(), $(e).triggerHandler("jqGridHeaderClick", [e.p.gridstate, a]), c && (Ea || e.p.onHeaderClick.call(e, e.p.gridstate, a)))
                        }) : "hidden" === e.p.gridstate && $(d, "#gbox_" + $.jgrid.jqID(e.p.id)).slideDown("fast", function () {
                            0 === --b && ($("span", g).removeClass(La).addClass(Ka), Ea && (e.p.datatype = Oa, V(), Ea = !1), e.p.gridstate = "visible", $("#gbox_" + $.jgrid.jqID(e.p.id)).hasClass("ui-resizable") && $(".ui-resizable-handle", "#gbox_" + $.jgrid.jqID(e.p.id)).show(), $(e).triggerHandler("jqGridHeaderClick", [e.p.gridstate, a]), c && (Ea || e.p.onHeaderClick.call(e, e.p.gridstate, a)))
                        }), !1
                    }), Ea && (e.p.datatype = "local", $(".ui-jqgrid-titlebar-close", f.cDiv).trigger("click")))
                } else $(f.cDiv).hide(), e.p.toppager || $(f.hDiv).addClass(l(e.p.styleUI + ".common", "cornertop", !0));
                if ($(f.hDiv).after(f.bDiv).mousemove(function (a) {
                    if (f.resizing) return f.dragMove(a), !1
                }), $(".ui-jqgrid-labels", f.hDiv).on("selectstart", function () {
                    return !1
                }), $(document).on("mouseup.jqGrid" + e.p.id, function () {
                    return !f.resizing || (f.dragEnd(!0), !1)
                }), "rtl" === e.p.direction && $(e).on("jqGridAfterGridComplete.setRTLPadding", function () {
                    var
                    a = f.bDiv.offsetWidth - f.bDiv.clientWidth;
                    e.p.scrollOffset = a, $("div:first", f.hDiv).css({
                        paddingLeft: a + "px"
                    }), f.hDiv.scrollLeft = f.bDiv.scrollLeft
                }), e.formatCol = B, e.sortData = Z, e.updatepager = Q, e.refreshIndex = L, e.setHeadCheckBox = W, e.constructTr = M, e.formatter = function (a, b, c, d, e) {
                    return D(a, b, c, d, e)
                }, $.extend(f, {
                    populate: V,
                    emptyRows: J,
                    beginReq: R,
                    endReq: S
                }), this.grid = f, e.addXmlData = function (a) {
                    N(a)
                }, e.addJSONData = function (a) {
                    O(a)
                }, e.addLocalData = function (a) {
                    return P(a)
                }, this.grid.cols = this.rows[0].cells, $.isFunction(e.p.onInitGrid) && e.p.onInitGrid.call(e), V(), e.p.hiddengrid = !1, e.p.responsive) {
                    var
                    Pa = "onorientationchange" in window,
                        Qa = Pa ? "orientationchange" : "resize";
                    $(window).on(Qa, function () {
                        $(e).jqGrid("resizeGrid")
                    })
                }
            }
        })
    }, $.jgrid.extend({
        getGridParam: function (a, b) {
            var
            c, d = this[0];
            if (d && d.grid) {
                if (void
                0 === b && "string" != typeof
                b && (b = "jqGrid"), c = d.p, "jqGrid" !== b) try {
                    c = $(d).data(b)
                } catch (a) {
                    c = d.p
                }
                return a ? void
                0 !== c[a] ? c[a] : null : c
            }
        },
        setGridParam: function (a, b) {
            return this.each(function () {
                if (null == b && (b = !1), this.grid && "object" == typeof
                a) if (!0 === b) {
                    var
                    c = $.extend({}, this.p, a);
                    this.p = c
                } else $.extend(!0, this.p, a)
            })
        },
        getGridRowById: function (a) {
            var
            b;
            return this.each(function () {
                try {
                    for (var
                    c = this.rows.length; c--;) if (a.toString() === this.rows[c].id) {
                        b = this.rows[c];
                        break
                    }
                } catch (c) {
                    b = $(this.grid.bDiv).find("#" + $.jgrid.jqID(a))
                }
            }), b
        },
        getDataIDs: function () {
            var
            a, b = [],
                c = 0,
                d = 0;
            return this.each(function () {
                if ((a = this.rows.length) && a > 0) for (; c < a;) $(this.rows[c]).hasClass("jqgrow") && (b[d] = this.rows[c].id, d++), c++
            }), b
        },
        setSelection: function (a, b, c) {
            return this.each(function () {
                function
                d(a) {
                    var
                    b = $(l.grid.bDiv)[0].clientHeight,
                        c = $(l.grid.bDiv)[0].scrollTop,
                        d = $(l.rows[a]).position().top,
                        e = l.rows[a].clientHeight;
                    d + e >= b + c ? $(l.grid.bDiv)[0].scrollTop = d - (b + c) + e + c : d < b + c && d < c && ($(l.grid.bDiv)[0].scrollTop = d)
                }
                var
                e, f, g, h, i, j, k, l = this,
                    m = $.jgrid.getMethod("getStyleUI"),
                    n = m(l.p.styleUI + ".common", "highlight", !0),
                    o = m(l.p.styleUI + ".common", "disabled", !0);
                void
                0 !== a && (b = !1 !== b, !(f = $(l).jqGrid("getGridRowById", a)) || !f.className || f.className.indexOf(o) > -1 || (!0 === l.p.scrollrows && (g = $(l).jqGrid("getGridRowById", a).rowIndex) >= 0 && d(g), !0 === l.p.frozenColumns && (j = l.p.id + "_frozen"), l.p.multiselect ? (l.setHeadCheckBox(!1), l.p.selrow = f.id, h = $.inArray(l.p.selrow, l.p.selarrrow), -1 === h ? ("ui-subgrid" !== f.className && $(f).addClass(n).attr("aria-selected", "true"), e = !0, l.p.selarrrow.push(l.p.selrow)) : ("ui-subgrid" !== f.className && $(f).removeClass(n).attr("aria-selected", "false"), e = !1, l.p.selarrrow.splice(h, 1), i = l.p.selarrrow[0], l.p.selrow = void
                0 === i ? null : i), $("#jqg_" + $.jgrid.jqID(l.p.id) + "_" + $.jgrid.jqID(f.id))[l.p.useProp ? "prop" : "attr"]("checked", e), j && (-1 === h ? $("#" + $.jgrid.jqID(a), "#" + $.jgrid.jqID(j)).addClass(n) : $("#" + $.jgrid.jqID(a), "#" + $.jgrid.jqID(j)).removeClass(n), $("#jqg_" + $.jgrid.jqID(l.p.id) + "_" + $.jgrid.jqID(a), "#" + $.jgrid.jqID(j))[l.p.useProp ? "prop" : "attr"]("checked", e)), b && ($(l).triggerHandler("jqGridSelectRow", [f.id, e, c]), l.p.onSelectRow && l.p.onSelectRow.call(l, f.id, e, c))) : "ui-subgrid" !== f.className && (l.p.selrow !== f.id ? (k = $(l).jqGrid("getGridRowById", l.p.selrow), k && $(k).removeClass(n).attr({
                    "aria-selected": "false",
                    tabindex: "-1"
                }), $(f).addClass(n).attr({
                    "aria-selected": "true",
                    tabindex: "0"
                }), j && ($("#" + $.jgrid.jqID(l.p.selrow), "#" + $.jgrid.jqID(j)).removeClass(n), $("#" + $.jgrid.jqID(a), "#" + $.jgrid.jqID(j)).addClass(n)), e = !0) : e = !1, l.p.selrow = f.id, b && ($(l).triggerHandler("jqGridSelectRow", [f.id, e, c]), l.p.onSelectRow && l.p.onSelectRow.call(l, f.id, e, c)))))
            })
        },
        resetSelection: function (a) {
            return this.each(function () {
                var
                b, c, d = this,
                    e = $.jgrid.getMethod("getStyleUI"),
                    f = e(d.p.styleUI + ".common", "highlight", !0),
                    g = e(d.p.styleUI + ".common", "hover", !0);
                if (!0 === d.p.frozenColumns && (c = d.p.id + "_frozen"), void
                0 !== a) {
                    if (b = a === d.p.selrow ? d.p.selrow : a, $("#" + $.jgrid.jqID(d.p.id) + " tbody:first tr#" + $.jgrid.jqID(b)).removeClass(f).attr("aria-selected", "false"), c && $("#" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(c)).removeClass(f), d.p.multiselect) {
                        $("#jqg_" + $.jgrid.jqID(d.p.id) + "_" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(d.p.id))[d.p.useProp ? "prop" : "attr"]("checked", !1), c && $("#jqg_" + $.jgrid.jqID(d.p.id) + "_" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(c))[d.p.useProp ? "prop" : "attr"]("checked", !1), d.setHeadCheckBox(!1);
                        var
                        h = $.inArray($.jgrid.jqID(b), d.p.selarrrow); - 1 !== h && d.p.selarrrow.splice(h, 1)
                    }
                    d.p.onUnSelectRow && d.p.onUnSelectRow.call(d, b), b = null
                } else d.p.multiselect ? ($(d.p.selarrrow).each(function (a, b) {
                    $($(d).jqGrid("getGridRowById", b)).removeClass(f).attr("aria-selected", "false"), $("#jqg_" + $.jgrid.jqID(d.p.id) + "_" + $.jgrid.jqID(b))[d.p.useProp ? "prop" : "attr"]("checked", !1), c && ($("#" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(c)).removeClass(f), $("#jqg_" + $.jgrid.jqID(d.p.id) + "_" + $.jgrid.jqID(b), "#" + $.jgrid.jqID(c))[d.p.useProp ? "prop" : "attr"]("checked", !1)), d.p.onUnSelectRow && d.p.onUnSelectRow.call(d, b)
                }), d.setHeadCheckBox(!1), d.p.selarrrow = [], d.p.selrow = null) : d.p.selrow && ($("#" + $.jgrid.jqID(d.p.id) + " tbody:first tr#" + $.jgrid.jqID(d.p.selrow)).removeClass(f).attr("aria-selected", "false"), c && $("#" + $.jgrid.jqID(d.p.selrow), "#" + $.jgrid.jqID(c)).removeClass(f), d.p.onUnSelectRow && d.p.onUnSelectRow.call(d, d.p.selrow), d.p.selrow = null);
                !0 === d.p.cellEdit && parseInt(d.p.iCol, 10) >= 0 && parseInt(d.p.iRow, 10) >= 0 && ($("td:eq(" + d.p.iCol + ")", d.rows[d.p.iRow]).removeClass("edit-cell " + f), $(d.rows[d.p.iRow]).removeClass("selected-row " + g)), d.p.savedRow = []
            })
        },
        getRowData: function (a, b) {
            var
            c, d, e = {}, f = !1,
                g = 0;
            return this.each(function () {
                var
                h, i, j = this;
                if (null == a) f = !0, c = [], d = j.rows.length - 1;
                else {
                    if (!(i = $(j).jqGrid("getGridRowById", a))) return e;
                    d = 1
                }
                for (b && !0 === b && j.p.data.length > 0 || (b = !1); g < d;) f && (i = j.rows[g + 1]), $(i).hasClass("jqgrow") && (b ? e = j.p.data[j.p._index[i.id]] : $('td[role="gridcell"]', i).each(function (a) {
                    if ("cb" !== (h = j.p.colModel[a].name) && "subgrid" !== h && "rn" !== h) if (!0 === j.p.treeGrid && h === j.p.ExpandColumn) e[h] = $.jgrid.htmlDecode($("span:first", this).html());
                    else try {
                        e[h] = $.unformat.call(j, this, {
                            rowId: i.id,
                            colModel: j.p.colModel[a]
                        }, a)
                    } catch (a) {
                        e[h] = $.jgrid.htmlDecode($(this).html())
                    }
                }), f && (c.push(e), e = {})), g++
            }), c || e
        },
        delRowData: function (a) {
            var
            b, c, d, e = !1;
            return this.each(function () {
                var
                f = this;
                if (!(b = $(f).jqGrid("getGridRowById", a))) return !1;
                if (f.p.subGrid && (d = $(b).next(), d.hasClass("ui-subgrid") && d.remove()), $(b).remove(), f.p.records--, f.p.reccount--, f.updatepager(!0, !1), e = !0, f.p.multiselect && -1 !== (c = $.inArray(a, f.p.selarrrow)) && f.p.selarrrow.splice(c, 1), f.p.multiselect && f.p.selarrrow.length > 0 ? f.p.selrow = f.p.selarrrow[f.p.selarrrow.length - 1] : f.p.selrow === a && (f.p.selrow = null), "local" === f.p.datatype) {
                    var
                    g = $.jgrid.stripPref(f.p.idPrefix, a),
                        h = f.p._index[g];
                    void
                    0 !== h && (f.p.data.splice(h, 1), f.refreshIndex())
                }
            }), e
        },
        setRowData: function (a, b, c) {
            var
            d, e, f = !0;
            return this.each(function () {
                if (!this.grid) return !1;
                var
                g, h, i = this,
                    j = typeof
                    c,
                    k = {};
                if (!(h = $(this).jqGrid("getGridRowById", a))) return !1;
                if (b) try {
                    if ($(this.p.colModel).each(function (c) {
                        d = this.name;
                        var
                        f = $.jgrid.getAccessor(b, d);
                        void
                        0 !== f && (k[d] = this.formatter && "string" == typeof
                        this.formatter && "date" === this.formatter ? $.unformat.date.call(i, f, this) : f, g = i.formatter(a, k[d], c, b, "edit"), e = this.title ? {
                            title: $.jgrid.stripHtml(g)
                        } : {}, !0 === i.p.treeGrid && d === i.p.ExpandColumn ? $("td[role='gridcell']:eq(" + c + ") > span:first", h).html(g).attr(e) : $("td[role='gridcell']:eq(" + c + ")", h).html(g).attr(e))
                    }), "local" === i.p.datatype) {
                        var
                        l, m = $.jgrid.stripPref(i.p.idPrefix, a),
                            n = i.p._index[m];
                        if (i.p.treeGrid) for (l in i.p.treeReader) i.p.treeReader.hasOwnProperty(l) && delete
                        k[i.p.treeReader[l]];
                        void
                        0 !== n && (i.p.data[n] = $.extend(!0, i.p.data[n], k)), k = null
                    }
                } catch (a) {
                    f = !1
                }
                f && ("string" === j ? $(h).addClass(c) : null !== c && "object" === j && $(h).css(c), $(i).triggerHandler("jqGridAfterGridComplete"))
            }), f
        },
        addRowData: function (a, b, c, d) {
            -1 === $.inArray(c, ["first", "last", "before", "after"]) && (c = "last");
            var
            e, f, g, h, i, j, k, l, m, n, o, p, q, r = !1,
                s = "",
                t = "",
                u = "";
            return b && ($.isArray(b) ? (m = !0, n = a) : (b = [b], m = !1), this.each(function () {
                var
                v = this,
                    w = b.length;
                i = !0 === v.p.rownumbers ? 1 : 0, g = !0 === v.p.multiselect ? 1 : 0, h = !0 === v.p.subGrid ? 1 : 0, m || (void
                0 !== a ? a = String(a) : (a = $.jgrid.randId(), !1 !== v.p.keyName && (n = v.p.keyName, void
                0 !== b[0][n] && (a = b[0][n]))));
                var
                x = 0,
                    y = $(v).jqGrid("getStyleUI", v.p.styleUI + ".base", "rowBox", !0, "jqgrow ui-row-" + v.p.direction),
                    z = {}, A = !! $.isFunction(v.p.afterInsertRow);
                for (i && (s = $(v).jqGrid("getStyleUI", v.p.styleUI + ".base", "rownumBox", !1, "jqgrid-rownum")), g && (t = $(v).jqGrid("getStyleUI", v.p.styleUI + ".base", "multiBox", !1, "cbox")); x < w;) {
                    if (o = b[x], f = [], m) try {
                        a = o[n], void
                        0 === a && (a = $.jgrid.randId())
                    } catch (b) {
                        a = $.jgrid.randId()
                    }
                    for (q = a, a = v.p.idPrefix + a, i && (u = v.formatCol(0, 1, "", null, a, !0), f[f.length] = '<td role="gridcell" ' + s + " " + u + ">0</td>"), g && (l = '<input role="checkbox" type="checkbox" id="jqg_' + v.p.id + "_" + a + '" ' + t + "/>", u = v.formatCol(i, 1, "", null, a, !0), f[f.length] = '<td role="gridcell" ' + u + ">" + l + "</td>"), h && (f[f.length] = $(v).jqGrid("addSubGridCell", g + i, 1)), k = g + h + i; k < v.p.colModel.length; k++) p = v.p.colModel[k], e = p.name, z[e] = o[e], l = v.formatter(a, $.jgrid.getAccessor(o, e), k, o), u = v.formatCol(k, 1, l, o, a, z), f[f.length] = '<td role="gridcell" ' + u + ">" + l + "</td>";
                    if (f.unshift(v.constructTr(a, !1, y, z, o)), f[f.length] = "</tr>", 0 === v.rows.length) $("table:first", v.grid.bDiv).append(f.join(""));
                    else switch (c) {
                        case "last":
                            $(v.rows[v.rows.length - 1]).after(f.join("")), j = v.rows.length - 1;
                            break;
                        case "first":
                            $(v.rows[0]).after(f.join("")), j = 1;
                            break;
                        case "after":
                            j = $(v).jqGrid("getGridRowById", d), j && ($(v.rows[j.rowIndex + 1]).hasClass("ui-subgrid") ? $(v.rows[j.rowIndex + 1]).after(f) : $(j).after(f.join("")), j = j.rowIndex + 1);
                            break;
                        case "before":
                            j = $(v).jqGrid("getGridRowById", d), j && ($(j).before(f.join("")), j = j.rowIndex - 1)
                    }!0 === v.p.subGrid && $(v).jqGrid("addSubGrid", g + i, j), v.p.records++, v.p.reccount++, $(v).triggerHandler("jqGridAfterInsertRow", [a, o, o]), A && v.p.afterInsertRow.call(v, a, o, o), x++, "local" === v.p.datatype && (z[v.p.localReader.id] = q, v.p._index[q] = v.p.data.length, v.p.data.push(z), z = {})
                }
                v.updatepager(!0, !0), r = !0
            })), r
        },
        footerData: function (a, b, c) {
            function
            d(a) {
                var
                b;
                for (b in a) if (a.hasOwnProperty(b)) return !1;
                return !0
            }
            var
            e, f, g = !1,
                h = {};
            return void
            0 === a && (a = "get"), "boolean" != typeof
            c && (c = !0), a = a.toLowerCase(), this.each(function () {
                var
                i, j = this;
                return !(!j.grid || !j.p.footerrow) && (("set" !== a || !d(b)) && (g = !0, void
                $(this.p.colModel).each(function (d) {
                    e = this.name, "set" === a ? void
                    0 !== b[e] && (i = c ? j.formatter("", b[e], d, b, "edit") : b[e], f = this.title ? {
                        title: $.jgrid.stripHtml(i)
                    } : {}, $("tr.footrow td:eq(" + d + ")", j.grid.sDiv).html(i).attr(f), g = !0) : "get" === a && (h[e] = $("tr.footrow td:eq(" + d + ")", j.grid.sDiv).html())
                })))
            }), "get" === a ? h : g
        },
        showHideCol: function (a, b) {
            return this.each(function () {
                var
                c, d = this,
                    e = !1,
                    f = $.jgrid.cell_width ? 0 : d.p.cellLayout;
                if (d.grid) {
                    "string" == typeof
                    a && (a = [a]), b = "none" !== b ? "" : "none";
                    var
                    g = "" === b,
                        h = d.p.groupHeader && ($.isArray(d.p.groupHeader) || $.isFunction(d.p.groupHeader));
                    if (h && $(d).jqGrid("destroyGroupHeader", !1), $(this.p.colModel).each(function (h) {
                        if (-1 !== $.inArray(this.name, a) && this.hidden === g) {
                            if (!0 === d.p.frozenColumns && !0 === this.frozen) return !0;
                            $("tr[role=row]", d.grid.hDiv).each(function () {
                                $(this.cells[h]).css("display", b)
                            }), $(d.rows).each(function () {
                                $(this).hasClass("jqgroup") || $(this.cells[h]).css("display", b)
                            }), d.p.footerrow && $("tr.footrow td:eq(" + h + ")", d.grid.sDiv).css("display", b), c = parseInt(this.width, 10), "none" === b ? d.p.tblwidth -= c + f : d.p.tblwidth += c + f, this.hidden = !g, e = !0, $(d).triggerHandler("jqGridShowHideCol", [g, this.name, h])
                        }
                    }), !0 === e && (!0 !== d.p.shrinkToFit || isNaN(d.p.height) || (d.p.tblwidth += parseInt(d.p.scrollOffset, 10)), $(d).jqGrid("setGridWidth", !0 === d.p.shrinkToFit ? d.p.tblwidth : d.p.width)), h) {
                        var
                        i = $.extend([], d.p.groupHeader);
                        d.p.groupHeader = null;
                        for (var
                        j = 0; j < i.length; j++) $(d).jqGrid("setGroupHeaders", i[j])
                    }
                }
            })
        },
        hideCol: function (a) {
            return this.each(function () {
                $(this).jqGrid("showHideCol", a, "none")
            })
        },
        showCol: function (a) {
            return this.each(function () {
                $(this).jqGrid("showHideCol", a, "")
            })
        },
        remapColumns: function (a, b, c) {
            function
            d(b) {
                var
                c;
                c = b.length ? $.makeArray(b) : $.extend({}, b), $.each(a, function (a) {
                    b[a] = c[this]
                })
            }

            function
            e(b, c) {
                $(">tr" + (c || ""), b).each(function () {
                    var
                    b = this,
                        c = $.makeArray(b.cells);
                    $.each(a, function () {
                        var
                        a = c[this];
                        a && b.appendChild(a)
                    })
                })
            }
            var
            f = this.get(0);
            d(f.p.colModel), d(f.p.colNames), d(f.grid.headers), e($("thead:first", f.grid.hDiv), c && ":not(.ui-jqgrid-labels)"), b && e($("#" + $.jgrid.jqID(f.p.id) + " tbody:first"), ".jqgfirstrow, tr.jqgrow, tr.jqfoot"), f.p.footerrow && e($("tbody:first", f.grid.sDiv)), f.p.remapColumns && (f.p.remapColumns.length ? d(f.p.remapColumns) : f.p.remapColumns = $.makeArray(a)), f.p.lastsort = $.inArray(f.p.lastsort, a), f.p.treeGrid && (f.p.expColInd = $.inArray(f.p.expColInd, a)), $(f).triggerHandler("jqGridRemapColumns", [a, b, c])
        },
        setGridWidth: function (a, b) {
            return this.each(function () {
                if (this.grid) {
                    var
                    c, d, e, f, g = this,
                        h = 0,
                        i = $.jgrid.cell_width ? 0 : g.p.cellLayout,
                        j = 0,
                        k = !1,
                        l = g.p.scrollOffset,
                        m = 0,
                        n = "Bootstrap" === g.p.styleUI ? 2 : 0;
                    if ("boolean" != typeof
                    b && (b = g.p.shrinkToFit), !isNaN(a)) {
                        if (a = parseInt(a, 10), g.grid.width = g.p.width = a, $("#gbox_" + $.jgrid.jqID(g.p.id)).css("width", a + "px"), $("#gview_" + $.jgrid.jqID(g.p.id)).css("width", a + "px"), $(g.grid.bDiv).css("width", a - n + "px"), $(g.grid.hDiv).css("width", a - n + "px"), g.p.pager && $(g.p.pager).css("width", a + "px"), g.p.toppager && $(g.p.toppager).css("width", a - n + "px"), !0 === g.p.toolbar[0] && ($(g.grid.uDiv).css("width", a - n + "px"), "both" === g.p.toolbar[1] && $(g.grid.ubDiv).css("width", a - n + "px")), g.p.footerrow && $(g.grid.sDiv).css("width", a - n + "px"), !1 === b && !0 === g.p.forceFit && (g.p.forceFit = !1), !0 === b) {
                            if ($.each(g.p.colModel, function () {
                                !1 === this.hidden && (c = this.widthOrg, h += c + i, this.fixed ? m += c + i : j++)
                            }), 0 === j) return;
                            g.p.tblwidth = h, e = a - i * j - m, isNaN(g.p.height) || ($(g.grid.bDiv)[0].clientHeight < $(g.grid.bDiv)[0].scrollHeight || 1 === g.rows.length) && (k = !0, e -= l), h = 0;
                            var
                            o = g.grid.cols.length > 0;
                            if ($.each(g.p.colModel, function (a) {
                                if (!1 === this.hidden && !this.fixed) {
                                    if (c = this.widthOrg, (c = Math.round(e * c / (g.p.tblwidth - i * j - m))) < 0) return;
                                    this.width = c, h += c, g.grid.headers[a].width = c, g.grid.headers[a].el.style.width = c + "px", g.p.footerrow && (g.grid.footers[a].style.width = c + "px"), o && (g.grid.cols[a].style.width = c + "px"), d = a
                                }
                            }), !d) return;
                            if (f = 0, k ? a - m - (h + i * j) !== l && (f = a - m - (h + i * j) - l) : 1 !== Math.abs(a - m - (h + i * j)) && (f = a - m - (h + i * j)), g.p.colModel[d].width += f, g.p.tblwidth = h + f + i * j + m, g.p.tblwidth > a) {
                                var
                                p = g.p.tblwidth - parseInt(a, 10);
                                g.p.tblwidth = a, c = g.p.colModel[d].width = g.p.colModel[d].width - p
                            } else c = g.p.colModel[d].width;
                            g.grid.headers[d].width = c, g.grid.headers[d].el.style.width = c + "px", o && (g.grid.cols[d].style.width = c + "px"), g.p.footerrow && (g.grid.footers[d].style.width = c + "px")
                        }
                        g.p.tblwidth && ($("table:first", g.grid.bDiv).css("width", g.p.tblwidth + "px"), $("table:first", g.grid.hDiv).css("width", g.p.tblwidth + "px"), g.grid.hDiv.scrollLeft = g.grid.bDiv.scrollLeft, g.p.footerrow && $("table:first", g.grid.sDiv).css("width", g.p.tblwidth + "px"))
                    }
                }
            })
        },
        setGridHeight: function (a) {
            return this.each(function () {
                var
                b = this;
                if (b.grid) {
                    var
                    c = $(b.grid.bDiv);
                    c.css({
                        height: a + (isNaN(a) ? "" : "px")
                    }), !0 === b.p.frozenColumns && $("#" + $.jgrid.jqID(b.p.id) + "_frozen").parent().height(c.height() - 16), b.p.height = a, b.p.scroll && b.grid.populateVisible()
                }
            })
        },
        setCaption: function (a) {
            return this.each(function () {
                var
                b = $(this).jqGrid("getStyleUI", this.p.styleUI + ".common", "cornertop", !0);
                this.p.caption = a, $(".ui-jqgrid-title, .ui-jqgrid-title-rtl", this.grid.cDiv).html(a), $(this.grid.cDiv).show(), $(this.grid.hDiv).removeClass(b)
            })
        },
        setLabel: function (a, b, c, d) {
            return this.each(function () {
                var
                e = this,
                    f = -1;
                if (e.grid && null != a && (isNaN(a) ? $(e.p.colModel).each(function (b) {
                    if (this.name === a) return f = b, !1
                }) : f = parseInt(a, 10), f >= 0)) {
                    var
                    g = $("tr.ui-jqgrid-labels th:eq(" + f + ")", e.grid.hDiv);
                    if (b) {
                        var
                        h = $(".s-ico", g);
                        $("[id^=jqgh_]", g).empty().html(b).append(h), e.p.colNames[f] = b
                    }
                    c && ("string" == typeof
                    c ? $(g).addClass(c) : $(g).css(c)), "object" == typeof
                    d && $(g).attr(d)
                }
            })
        },
        setSortIcon: function (a, b) {
            return this.each(function () {
                var
                c = this,
                    d = -1;
                if (c.grid && null != a && (isNaN(a) ? $(c.p.colModel).each(function (b) {
                    if (this.name === a) return d = b, !1
                }) : d = parseInt(a, 10), d >= 0)) {
                    var
                    e = $("tr.ui-jqgrid-labels th:eq(" + d + ")", c.grid.hDiv);
                    "left" === b ? e.find(".s-ico").css("float", "left") : e.find(".s-ico").css("float", "none")
                }
            })
        },
        setCell: function (a, b, c, d, e, f) {
            return this.each(function () {
                var
                g, h, i = this,
                    j = -1;
                if (i.grid && (isNaN(b) ? $(i.p.colModel).each(function (a) {
                    if (this.name === b) return j = a, !1
                }) : j = parseInt(b, 10), j >= 0)) {
                    var
                    k = $(i).jqGrid("getGridRowById", a);
                    if (k) {
                        var
                        l = $("td:eq(" + j + ")", k),
                            m = 0,
                            n = [];
                        if ("" !== c || !0 === f) {
                            if (void
                            0 !== k.cells) for (; m < k.cells.length;) n.push(k.cells[m].innerHTML), m++;
                            if (g = i.formatter(a, c, j, n, "edit"), h = i.p.colModel[j].title ? {
                                title: $.jgrid.stripHtml(g)
                            } : {}, i.p.treeGrid && $(".tree-wrap", $(l)).length > 0 ? $("span", $(l)).html(g).attr(h) : $(l).html(g).attr(h), "local" === i.p.datatype) {
                                var
                                o, p = i.p.colModel[j];
                                c = p.formatter && "string" == typeof
                                p.formatter && "date" === p.formatter ? $.unformat.date.call(i, c, p) : c, o = i.p._index[$.jgrid.stripPref(i.p.idPrefix, a)], void
                                0 !== o && (i.p.data[o][p.name] = c)
                            }
                        }
                        "string" == typeof
                        d ? $(l).addClass(d) : d && $(l).css(d), "object" == typeof
                        e && $(l).attr(e)
                    }
                }
            })
        },
        getCell: function (a, b) {
            var
            c = !1;
            return this.each(function () {
                var
                d, e, f = this,
                    g = -1;
                if (f.grid && (d = b, isNaN(b) ? $(f.p.colModel).each(function (a) {
                    if (this.name === b) return d = this.name, g = a, !1
                }) : g = parseInt(b, 10), g >= 0)) {
                    if (e = $(f).jqGrid("getGridRowById", a)) try {
                        c = $.unformat.call(f, $("td:eq(" + g + ")", e), {
                            rowId: e.id,
                            colModel: f.p.colModel[g]
                        }, g)
                    } catch (a) {
                        c = $.jgrid.htmlDecode($("td:eq(" + g + ")", e).html())
                    }
                    f.p.treeGrid && c && f.p.ExpandColumn === d && (c = $("<div>" + c + "</div>").find("span:first").html())
                }
            }), c
        },
        getCol: function (a, b, c) {
            var
            d, e, f, g, h = [],
                i = 0;
            return b = "boolean" == typeof
            b && b, void
            0 === c && (c = !1), this.each(function () {
                var
                j = this,
                    k = -1;
                if (j.grid && (isNaN(a) ? $(j.p.colModel).each(function (b) {
                    if (this.name === a) return k = b, !1
                }) : k = parseInt(a, 10), k >= 0)) {
                    var
                    l = j.rows.length,
                        m = 0,
                        n = 0;
                    if (l && l > 0) {
                        for (; m < l;) {
                            if ($(j.rows[m]).hasClass("jqgrow")) {
                                try {
                                    d = $.unformat.call(j, $(j.rows[m].cells[k]), {
                                        rowId: j.rows[m].id,
                                        colModel: j.p.colModel[k]
                                    }, k)
                                } catch (a) {
                                    d = $.jgrid.htmlDecode(j.rows[m].cells[k].innerHTML)
                                }
                                c ? (g = parseFloat(d), isNaN(g) || (i += g, void
                                0 === f && (f = e = g), e = Math.min(e, g), f = Math.max(f, g), n++)) : b ? h.push({
                                    id: j.rows[m].id,
                                    value: d
                                }) : h.push(d)
                            }
                            m++
                        }
                        if (c) switch (c.toLowerCase()) {
                            case "sum":
                                h = i;
                                break;
                            case "avg":
                                h = i / n;
                                break;
                            case "count":
                                h = l - 1;
                                break;
                            case "min":
                                h = e;
                                break;
                            case "max":
                                h = f
                        }
                    }
                }
            }), h
        },
        clearGridData: function (a) {
            return this.each(function () {
                var
                b = this;
                if (b.grid) {
                    if ("boolean" != typeof
                    a && (a = !1), b.p.deepempty) $("#" + $.jgrid.jqID(b.p.id) + " tbody:first tr:gt(0)").remove();
                    else {
                        var
                        c = $("#" + $.jgrid.jqID(b.p.id) + " tbody:first tr:first")[0];
                        $("#" + $.jgrid.jqID(b.p.id) + " tbody:first").empty().append(c)
                    }
                    b.p.footerrow && a && $(".ui-jqgrid-ftable td", b.grid.sDiv).html("&#160;"), b.p.selrow = null, b.p.selarrrow = [], b.p.savedRow = [], b.p.records = 0, b.p.page = 1, b.p.lastpage = 0, b.p.reccount = 0, b.p.data = [], b.p._index = {}, b.updatepager(!0, !1)
                }
            })
        },
        getInd: function (a, b) {
            var
            c, d = !1;
            return this.each(function () {
                (c = $(this).jqGrid("getGridRowById", a)) && (d = !0 === b ? c : c.rowIndex)
            }), d
        },
        bindKeys: function (a) {
            var
            b = $.extend({
                onEnter: null,
                onSpace: null,
                onLeftKey: null,
                onRightKey: null,
                scrollingRows: !0
            }, a || {});
            return this.each(function () {
                var
                a = this;
                $("body").is("[role]") || $("body").attr("role", "application"), a.p.scrollrows = b.scrollingRows, $(a).keydown(function (c) {
                    var
                    d, e, f, g = $(a).find("tr[tabindex=0]")[0],
                        h = a.p.treeReader.expanded_field;
                    if (g) if (f = a.p._index[$.jgrid.stripPref(a.p.idPrefix, g.id)], 37 === c.keyCode || 38 === c.keyCode || 39 === c.keyCode || 40 === c.keyCode) {
                        if (38 === c.keyCode) {
                            if (e = g.previousSibling, d = "", e) if ($(e).is(":hidden")) {
                                for (; e;) if (e = e.previousSibling, !$(e).is(":hidden") && $(e).hasClass("jqgrow")) {
                                    d = e.id;
                                    break
                                }
                            } else d = e.id;
                            $(a).jqGrid("setSelection", d, !0, c), c.preventDefault()
                        }
                        if (40 === c.keyCode) {
                            if (e = g.nextSibling, d = "", e) if ($(e).is(":hidden")) {
                                for (; e;) if (e = e.nextSibling, !$(e).is(":hidden") && $(e).hasClass("jqgrow")) {
                                    d = e.id;
                                    break
                                }
                            } else d = e.id;
                            $(a).jqGrid("setSelection", d, !0, c), c.preventDefault()
                        }
                        37 === c.keyCode && (a.p.treeGrid && a.p.data[f][h] && $(g).find("div.treeclick").trigger("click"), $(a).triggerHandler("jqGridKeyLeft", [a.p.selrow]), $.isFunction(b.onLeftKey) && b.onLeftKey.call(a, a.p.selrow)), 39 === c.keyCode && (a.p.treeGrid && !a.p.data[f][h] && $(g).find("div.treeclick").trigger("click"), $(a).triggerHandler("jqGridKeyRight", [a.p.selrow]), $.isFunction(b.onRightKey) && b.onRightKey.call(a, a.p.selrow))
                    } else 13 === c.keyCode ? ($(a).triggerHandler("jqGridKeyEnter", [a.p.selrow]), $.isFunction(b.onEnter) && b.onEnter.call(a, a.p.selrow)) : 32 === c.keyCode && ($(a).triggerHandler("jqGridKeySpace", [a.p.selrow]), $.isFunction(b.onSpace) && b.onSpace.call(a, a.p.selrow))
                })
            })
        },
        unbindKeys: function () {
            return this.each(function () {
                $(this).off("keydown")
            })
        },
        getLocalRow: function (a) {
            var
            b, c = !1;
            return this.each(function () {
                void
                0 !== a && (b = this.p._index[$.jgrid.stripPref(this.p.idPrefix, a)]) >= 0 && (c = this.p.data[b])
            }), c
        },
        progressBar: function (a) {
            return a = $.extend({
                htmlcontent: "",
                method: "hide",
                loadtype: "disable"
            }, a || {}), this.each(function () {
                var
                b, c, d = "show" === a.method,
                    e = $("#load_" + $.jgrid.jqID(this.p.id)),
                    f = $(window).scrollTop();
                switch ("" !== a.htmlcontent && e.html(a.htmlcontent), a.loadtype) {
                    case "disable":
                        break;
                    case "enable":
                        e.toggle(d);
                        break;
                    case "block":
                        $("#lui_" + $.jgrid.jqID(this.p.id)).toggle(d), e.toggle(d)
                }
                e.is(":visible") && (b = e.offsetParent(), e.css("top", ""), e.offset().top < f && (c = Math.min(10 + f - b.offset().top, b.height() - e.height()), e.css("top", c + "px")))
            })
        },
        getColProp: function (a) {
            var
            b = {}, c = this[0];
            if (!c.grid) return !1;
            var
            d, e = c.p.colModel;
            for (d = 0; d < e.length; d++) if (e[d].name === a) {
                b = e[d];
                break
            }
            return b
        },
        setColProp: function (a, b) {
            return this.each(function () {
                if (this.grid && $.isPlainObject(b)) {
                    var
                    c, d = this.p.colModel;
                    for (c = 0; c < d.length; c++) if (d[c].name === a) {
                        $.extend(!0, this.p.colModel[c], b);
                        break
                    }
                }
            })
        },
        sortGrid: function (a, b, c) {
            return this.each(function () {
                var
                d, e = this,
                    f = -1,
                    g = !1;
                if (e.grid) {
                    for (a || (a = e.p.sortname), d = 0; d < e.p.colModel.length; d++) if (e.p.colModel[d].index === a || e.p.colModel[d].name === a) {
                        f = d, !0 === e.p.frozenColumns && !0 === e.p.colModel[d].frozen && (g = e.grid.fhDiv.find("#" + e.p.id + "_" + a));
                        break
                    }
                    if (-1 !== f) {
                        var
                        h = e.p.colModel[f].sortable;
                        g || (g = e.grid.headers[f].el), "boolean" != typeof
                        h && (h = !0), "boolean" != typeof
                        b && (b = !1), h && e.sortData("jqgh_" + e.p.id + "_" + a, f, b, c, g)
                    }
                }
            })
        },
        setGridState: function (a) {
            return this.each(function () {
                if (this.grid) {
                    var
                    b = this,
                        c = $(this).jqGrid("getStyleUI", this.p.styleUI + ".base", "icon_caption_open", !0),
                        d = $(this).jqGrid("getStyleUI", this.p.styleUI + ".base", "icon_caption_close", !0);
                    "hidden" === a ? ($(".ui-jqgrid-bdiv, .ui-jqgrid-hdiv", "#gview_" + $.jgrid.jqID(b.p.id)).slideUp("fast"), b.p.pager && $(b.p.pager).slideUp("fast"), b.p.toppager && $(b.p.toppager).slideUp("fast"), !0 === b.p.toolbar[0] && ("both" === b.p.toolbar[1] && $(b.grid.ubDiv).slideUp("fast"), $(b.grid.uDiv).slideUp("fast")), b.p.footerrow && $(".ui-jqgrid-sdiv", "#gbox_" + $.jgrid.jqID(b.p.id)).slideUp("fast"), $(".ui-jqgrid-headlink", b.grid.cDiv).removeClass(c).addClass(d), b.p.gridstate = "hidden") : "visible" === a && ($(".ui-jqgrid-hdiv, .ui-jqgrid-bdiv", "#gview_" + $.jgrid.jqID(b.p.id)).slideDown("fast"), b.p.pager && $(b.p.pager).slideDown("fast"), b.p.toppager && $(b.p.toppager).slideDown("fast"), !0 === b.p.toolbar[0] && ("both" === b.p.toolbar[1] && $(b.grid.ubDiv).slideDown("fast"), $(b.grid.uDiv).slideDown("fast")), b.p.footerrow && $(".ui-jqgrid-sdiv", "#gbox_" + $.jgrid.jqID(b.p.id)).slideDown("fast"), $(".ui-jqgrid-headlink", b.grid.cDiv).removeClass(d).addClass(c), b.p.gridstate = "visible")
                }
            })
        },
        setFrozenColumns: function () {
            return this.each(function () {
                if (this.grid) {
                    var
                    a = this,
                        b = a.p.colModel,
                        c = 0,
                        d = b.length,
                        e = -1,
                        f = !1,
                        g = $(a).jqGrid("getStyleUI", a.p.styleUI + ".base", "headerDiv", !0, "ui-jqgrid-hdiv"),
                        h = $(a).jqGrid("getStyleUI", a.p.styleUI + ".common", "hover", !0),
                        i = "border-box" === $("#gbox_" + $.jgrid.jqID(a.p.id)).css("box-sizing"),
                        j = i ? 1 : 0;
                    if (!0 !== a.p.subGrid && !0 !== a.p.treeGrid && !0 !== a.p.cellEdit && !a.p.sortable && !a.p.scroll && !0 !== a.p.grouping) {
                        for (; c < d && !0 === b[c].frozen;) f = !0, e = c, c++;
                        if (e >= 0 && f) {
                            var
                            k = a.p.caption ? $(a.grid.cDiv).outerHeight() : 0,
                                l = parseInt($(".ui-jqgrid-htable", "#gview_" + $.jgrid.jqID(a.p.id)).height(), 10),
                                m = parseInt($(".ui-jqgrid-hdiv", "#gview_" + $.jgrid.jqID(a.p.id)).height(), 10);
                            a.p.toppager && (k += $(a.grid.topDiv).outerHeight()), !0 === a.p.toolbar[0] && "bottom" !== a.p.toolbar[1] && (k += $(a.grid.uDiv).outerHeight()), a.grid.fhDiv = $('<div style="position:absolute;' + ("rtl" === a.p.direction ? "right:0;" : "left:0;") + "top:" + k + "px;height:" + (m - j) + 'px;" class="frozen-div ' + g + '"></div>'), a.grid.fbDiv = $('<div style="position:absolute;' + ("rtl" === a.p.direction ? "right:0;" : "left:0;") + "top:" + (parseInt(k, 10) + parseInt(m, 10) + 1 - j) + 'px;overflow-y:hidden" class="frozen-bdiv ui-jqgrid-bdiv"></div>'), $("#gview_" + $.jgrid.jqID(a.p.id)).append(a.grid.fhDiv);
                            var
                            n = $(".ui-jqgrid-htable", "#gview_" + $.jgrid.jqID(a.p.id)).clone(!0);
                            if (a.p.groupHeader) {
                                $("tr.jqg-first-row-header, tr.jqg-third-row-header", n).each(function () {
                                    $("th:gt(" + e + ")", this).remove()
                                });
                                var
                                o, p, q = -1,
                                    r = -1;
                                $("tr.jqg-second-row-header th", n).each(function () {
                                    if (o = parseInt($(this).attr("colspan"), 10), p = parseInt($(this).attr("rowspan"), 10), p && (q++, r++), o && (q += o, r++), q === e) return r = e, !1
                                }), q !== e && (r = e), $("tr.jqg-second-row-header", n).each(function () {
                                    $("th:gt(" + r + ")", this).remove()
                                })
                            } else {
                                var
                                s = [];
                                $(".ui-jqgrid-htable tr", "#gview_" + $.jgrid.jqID(a.p.id)).each(function (a, b) {
                                    s.push(parseInt($(this).height(), 10))
                                }), $("tr", n).each(function () {
                                    $("th:gt(" + e + ")", this).remove()
                                }), $("tr", n).each(function (a) {
                                    $(this).height(s[a])
                                })
                            }
                            if ($(n).width(1), $.jgrid.msie() || $(n).css("height", "100%"), $(a.grid.fhDiv).append(n).mousemove(function (b) {
                                if (a.grid.resizing) return a.grid.dragMove(b), !1
                            }), a.p.footerrow) {
                                var
                                t = $(".ui-jqgrid-bdiv", "#gview_" + $.jgrid.jqID(a.p.id)).height();
                                a.grid.fsDiv = $('<div style="position:absolute;left:0px;top:' + (parseInt(k, 10) + parseInt(l, 10) + parseInt(t, 10) + 1 - j) + 'px;" class="frozen-sdiv ui-jqgrid-sdiv"></div>'), $("#gview_" + $.jgrid.jqID(a.p.id)).append(a.grid.fsDiv);
                                var
                                u = $(".ui-jqgrid-ftable", "#gview_" + $.jgrid.jqID(a.p.id)).clone(!0);
                                $("tr", u).each(function () {
                                    $("td:gt(" + e + ")", this).remove()
                                }), $(u).width(1), $(a.grid.fsDiv).append(u)
                            }
                            $(a).on("jqGridResizeStop.setFrozenColumns", function (b, c, d) {
                                var
                                e = i ? "outerWidth" : "width",
                                    f = $(".ui-jqgrid-htable", a.grid.fhDiv),
                                    g = $(".ui-jqgrid-btable", a.grid.fbDiv);
                                if ($("th:eq(" + d + ")", f)[e](c), $("tr:first td:eq(" + d + ")", g)[e](c), a.p.footerrow) {
                                    var
                                    h = $(".ui-jqgrid-ftable", a.grid.fsDiv);
                                    $("tr:first td:eq(" + d + ")", h)[e](c)
                                }
                            }), $("#gview_" + $.jgrid.jqID(a.p.id)).append(a.grid.fbDiv), $(a.grid.fbDiv).on("mousewheel DOMMouseScroll", function (b) {
                                var
                                c = $(a.grid.bDiv).scrollTop();
                                b.originalEvent.wheelDelta > 0 || b.originalEvent.detail < 0 ? $(a.grid.bDiv).scrollTop(c - 25) : $(a.grid.bDiv).scrollTop(c + 25), b.preventDefault()
                            }), !0 === a.p.hoverrows && $("#" + $.jgrid.jqID(a.p.id)).off("mouseover mouseout"), $(a).on("jqGridAfterGridComplete.setFrozenColumns", function () {
                                $("#" + $.jgrid.jqID(a.p.id) + "_frozen").remove(), $(a.grid.fbDiv).height($(a.grid.bDiv).height() - 17);
                                var
                                b = [];
                                $("#" + $.jgrid.jqID(a.p.id) + " tr[role=row].jqgrow").each(function () {
                                    b.push($(this).outerHeight())
                                });
                                var
                                c = $("#" + $.jgrid.jqID(a.p.id)).clone(!0);
                                $("tr[role=row]", c).each(function () {
                                    $("td[role=gridcell]:gt(" + e + ")", this).remove()
                                }), $(c).width(1).attr("id", a.p.id + "_frozen"), $(a.grid.fbDiv).append(c), $("tr[role=row].jqgrow", c).each(function (a, c) {
                                    $(this).height(b[a])
                                }), !0 === a.p.hoverrows && ($("tr.jqgrow", c).hover(function () {
                                    $(this).addClass(h), $("#" + $.jgrid.jqID(this.id), "#" + $.jgrid.jqID(a.p.id)).addClass(h)
                                }, function () {
                                    $(this).removeClass(h), $("#" + $.jgrid.jqID(this.id), "#" + $.jgrid.jqID(a.p.id)).removeClass(h)
                                }), $("tr.jqgrow", "#" + $.jgrid.jqID(a.p.id)).hover(function () {
                                    $(this).addClass(h), $("#" + $.jgrid.jqID(this.id), "#" + $.jgrid.jqID(a.p.id) + "_frozen").addClass(h)
                                }, function () {
                                    $(this).removeClass(h), $("#" + $.jgrid.jqID(this.id), "#" + $.jgrid.jqID(a.p.id) + "_frozen").removeClass(h)
                                })), c = null
                            }), a.grid.hDiv.loading || $(a).triggerHandler("jqGridAfterGridComplete"), a.p.frozenColumns = !0
                        }
                    }
                }
            })
        },
        destroyFrozenColumns: function () {
            return this.each(function () {
                if (this.grid && !0 === this.p.frozenColumns) {
                    var
                    a = this,
                        b = $(a).jqGrid("getStyleUI", a.p.styleUI + ".common", "hover", !0);
                    if ($(a.grid.fhDiv).remove(), $(a.grid.fbDiv).remove(), a.grid.fhDiv = null, a.grid.fbDiv = null, a.p.footerrow && ($(a.grid.fsDiv).remove(), a.grid.fsDiv = null), $(this).off(".setFrozenColumns"), !0 === a.p.hoverrows) {
                        var
                        c;
                        $("#" + $.jgrid.jqID(a.p.id)).on({
                            mouseover: function (a) {
                                c = $(a.target).closest("tr.jqgrow"), "ui-subgrid" !== $(c).attr("class") && $(c).addClass(b)
                            },
                            mouseout: function (a) {
                                c = $(a.target).closest("tr.jqgrow"), $(c).removeClass(b)
                            }
                        })
                    }
                    this.p.frozenColumns = !1
                }
            })
        },
        resizeColumn: function (a, b, c) {
            return this.each(function () {
                var
                d, e, f = this.grid,
                    g = this.p,
                    h = g.colModel,
                    i = h.length;
                if ("string" == typeof
                a) {
                    for (d = 0; d < i; d++) if (h[d].name === a) {
                        a = d;
                        break
                    }
                } else a = parseInt(a, 10);
                if (void
                0 === c && (c = !1), (h[a].resizable || c) && (b = parseInt(b, 10), !("number" != typeof
                a || a < 0 || a > h.length - 1 || "number" != typeof
                b || b < g.minColWidth))) {
                    if (g.forceFit) for (g.nv = 0, d = a + 1; d < i; d++) if (!0 !== h[d].hidden) {
                        g.nv = d - a;
                        break
                    }
                    if (f.resizing = {
                        idx: a
                    }, e = b - f.headers[a].width, g.forceFit) {
                        if (f.headers[a + g.nv].width - e < g.minColWidth) return;
                        f.headers[a + g.nv].newWidth = f.headers[a + g.nv].width - e
                    }
                    f.newWidth = g.tblwidth + e, f.headers[a].newWidth = b, f.dragEnd(!1)
                }
            })
        },
        getStyleUI: function (a, b, c, d) {
            var
            e = "",
                f = "";
            try {
                var
                g = a.split(".");
                switch (c || (e = "class=", f = '"'), null == d && (d = ""), g.length) {
                    case
                    1:
                        e += f + $.trim(d + " " + $.jgrid.styleUI[g[0]][b] + f);
                        break;
                    case
                    2:
                        e += f + $.trim(d + " " + $.jgrid.styleUI[g[0]][g[1]][b] + f)
                }
            } catch (a) {
                e = ""
            }
            return e
        },
        resizeGrid: function (a) {
            return this.each(function () {
                var
                b = this;
                void
                0 === a && (a = 500), setTimeout(function () {
                    try {
                        var
                        a = $(window).width(),
                            c = $("#gbox_" + $.jgrid.jqID(b.p.id)).parent().width(),
                            d = b.p.width;
                        d = a - c > 3 ? c : a, $("#" + $.jgrid.jqID(b.p.id)).jqGrid("setGridWidth", d)
                    } catch (a) {}
                }, a)
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.fmatter = {}, a.extend(a.fmatter, {
        isBoolean: function (a) {
            return "boolean" == typeof
            a
        },
        isObject: function (b) {
            return b && ("object" == typeof
            b || a.isFunction(b)) || !1
        },
        isString: function (a) {
            return "string" == typeof
            a
        },
        isNumber: function (a) {
            return "number" == typeof
            a && isFinite(a)
        },
        isValue: function (a) {
            return this.isObject(a) || this.isString(a) || this.isNumber(a) || this.isBoolean(a)
        },
        isEmpty: function (b) {
            return !(!this.isString(b) && this.isValue(b)) && (!this.isValue(b) || "" === (b = a.trim(b).replace(/\&nbsp\;/gi, "").replace(/\&#160\;/gi, "")))
        }
    }), a.fn.fmatter = function (b, c, d, e, f) {
        var
        g = c;
        d = a.extend({}, a.jgrid.getRegional(this, "formatter"), d);
        try {
            g = a.fn.fmatter[b].call(this, c, d, e, f)
        } catch (a) {}
        return g
    }, a.fmatter.util = {
        NumberFormat: function (b, c) {
            if (a.fmatter.isNumber(b) || (b *= 1), a.fmatter.isNumber(b)) {
                var
                d, e = b < 0,
                    f = String(b),
                    g = c.decimalSeparator || ".";
                if (a.fmatter.isNumber(c.decimalPlaces)) {
                    var
                    h = c.decimalPlaces,
                        i = Math.pow(10, h);
                    if (f = String(Math.round(b * i) / i), d = f.lastIndexOf("."), h > 0) for (d < 0 ? (f += g, d = f.length - 1) : "." !== g && (f = f.replace(".", g)); f.length - 1 - d < h;) f += "0"
                }
                if (c.thousandsSeparator) {
                    var
                    j = c.thousandsSeparator;
                    d = f.lastIndexOf(g), d = d > -1 ? d : f.length;
                    var
                    k, l = f.substring(d),
                        m = -1;
                    for (k = d; k > 0; k--) m++, m % 3 == 0 && k !== d && (!e || k > 1) && (l = j + l), l = f.charAt(k - 1) + l;
                    f = l
                }
                return f = c.prefix ? c.prefix + f : f, f = c.suffix ? f + c.suffix : f
            }
            return b
        }
    }, a.fn.fmatter.defaultFormat = function (b, c) {
        return a.fmatter.isValue(b) && "" !== b ? b : c.defaultValue || "&#160;"
    }, a.fn.fmatter.email = function (b, c) {
        return a.fmatter.isEmpty(b) ? a.fn.fmatter.defaultFormat(b, c) : '<a href="mailto:' + b + '">' + b + "</a>"
    }, a.fn.fmatter.checkbox = function (b, c) {
        var
        d, e = a.extend({}, c.checkbox);
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (e = a.extend({}, e, c.colModel.formatoptions)), d = !0 === e.disabled ? 'disabled="disabled"' : "", (a.fmatter.isEmpty(b) || void
        0 === b) && (b = a.fn.fmatter.defaultFormat(b, e)), b = String(b), b = (b + "").toLowerCase(), '<input type="checkbox" ' + (b.search(/(false|f|0|no|n|off|undefined)/i) < 0 ? " checked='checked' " : "") + ' value="' + b + '" offval="no" ' + d + "/>"
    }, a.fn.fmatter.link = function (b, c) {
        var
        d = {
            target: c.target
        }, e = "";
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (d = a.extend({}, d, c.colModel.formatoptions)), d.target && (e = "target=" + d.target), a.fmatter.isEmpty(b) ? a.fn.fmatter.defaultFormat(b, c) : "<a " + e + ' href="' + b + '">' + b + "</a>"
    }, a.fn.fmatter.showlink = function (b, c) {
        var
        d, e = {
            baseLinkUrl: c.baseLinkUrl,
            showAction: c.showAction,
            addParam: c.addParam || "",
            target: c.target,
            idName: c.idName
        }, f = "";
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (e = a.extend({}, e, c.colModel.formatoptions)), e.target && (f = "target=" + e.target), d = e.baseLinkUrl + e.showAction + "?" + e.idName + "=" + c.rowId + e.addParam, a.fmatter.isString(b) || a.fmatter.isNumber(b) ? "<a " + f + ' href="' + d + '">' + b + "</a>" : a.fn.fmatter.defaultFormat(b, c)
    }, a.fn.fmatter.integer = function (b, c) {
        var
        d = a.extend({}, c.integer);
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (d = a.extend({}, d, c.colModel.formatoptions)), a.fmatter.isEmpty(b) ? d.defaultValue : a.fmatter.util.NumberFormat(b, d)
    }, a.fn.fmatter.number = function (b, c) {
        var
        d = a.extend({}, c.number);
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (d = a.extend({}, d, c.colModel.formatoptions)), a.fmatter.isEmpty(b) ? d.defaultValue : a.fmatter.util.NumberFormat(b, d)
    }, a.fn.fmatter.currency = function (b, c) {
        var
        d = a.extend({}, c.currency);
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (d = a.extend({}, d, c.colModel.formatoptions)), a.fmatter.isEmpty(b) ? d.defaultValue : a.fmatter.util.NumberFormat(b, d)
    }, a.fn.fmatter.date = function (b, c, d, e) {
        var
        f = a.extend({}, c.date);
        return void
        0 !== c.colModel && void
        0 !== c.colModel.formatoptions && (f = a.extend({}, f, c.colModel.formatoptions)), f.reformatAfterEdit || "edit" !== e ? a.fmatter.isEmpty(b) ? a.fn.fmatter.defaultFormat(b, c) : a.jgrid.parseDate.call(this, f.srcformat, b, f.newformat, f) : a.fn.fmatter.defaultFormat(b, c)
    }, a.fn.fmatter.select = function (b, c) {
        b = String(b);
        var
        d, e, f = !1,
            g = [];
        if (void
        0 !== c.colModel.formatoptions ? (f = c.colModel.formatoptions.value, d = void
        0 === c.colModel.formatoptions.separator ? ":" : c.colModel.formatoptions.separator, e = void
        0 === c.colModel.formatoptions.delimiter ? ";" : c.colModel.formatoptions.delimiter) : void
        0 !== c.colModel.editoptions && (f = c.colModel.editoptions.value, d = void
        0 === c.colModel.editoptions.separator ? ":" : c.colModel.editoptions.separator, e = void
        0 === c.colModel.editoptions.delimiter ? ";" : c.colModel.editoptions.delimiter), f) {
            var
            h, i = !0 == (null != c.colModel.editoptions && !0 === c.colModel.editoptions.multiple),
                j = [];
            if (i && (j = b.split(","), j = a.map(j, function (b) {
                return a.trim(b)
            })), a.fmatter.isString(f)) {
                var
                k, l = f.split(e),
                    m = 0;
                for (k = 0; k < l.length; k++) if (h = l[k].split(d), h.length > 2 && (h[1] = a.map(h, function (a, b) {
                    if (b > 0) return a
                }).join(d)), i) a.inArray(h[0], j) > -1 && (g[m] = h[1], m++);
                else if (a.trim(h[0]) === a.trim(b)) {
                    g[0] = h[1];
                    break
                }
            } else a.fmatter.isObject(f) && (i ? g = a.map(j, function (a) {
                return f[a]
            }) : g[0] = f[b] || "")
        }
        return b = g.join(", "), "" === b ? a.fn.fmatter.defaultFormat(b, c) : b
    }, a.fn.fmatter.rowactions = function (b) {
        var
        c = a(this).closest("tr.jqgrow"),
            d = c.attr("id"),
            e = a(this).closest("table.ui-jqgrid-btable").attr("id").replace(/_frozen([^_]*)$/, "$1"),
            f = a("#" + e),
            g = f[0],
            h = g.p,
            i = h.colModel[a.jgrid.getCellIndex(this)],
            j = i.frozen ? a("tr#" + d + " td:eq(" + a.jgrid.getCellIndex(this) + ") > div", f) : a(this).parent(),
            k = {
                extraparam: {}
            }, l = function (b, c) {
                a.isFunction(k.afterSave) && k.afterSave.call(g, b, c), j.find("div.ui-inline-edit,div.ui-inline-del").show(), j.find("div.ui-inline-save,div.ui-inline-cancel").hide()
            }, m = function (b) {
                a.isFunction(k.afterRestore) && k.afterRestore.call(g, b), j.find("div.ui-inline-edit,div.ui-inline-del").show(), j.find("div.ui-inline-save,div.ui-inline-cancel").hide()
            };
        if (void
        0 !== i.formatoptions) {
            var
            n = a.extend(!0, {}, i.formatoptions);
            k = a.extend(k, n)
        }
        void
        0 !== h.editOptions && (k.editOptions = h.editOptions), void
        0 !== h.delOptions && (k.delOptions = h.delOptions), c.hasClass("jqgrid-new-row") && (k.extraparam[h.prmNames.oper] = h.prmNames.addoper);
        var
        o = {
            keys: k.keys,
            oneditfunc: k.onEdit,
            successfunc: k.onSuccess,
            url: k.url,
            extraparam: k.extraparam,
            aftersavefunc: l,
            errorfunc: k.onError,
            afterrestorefunc: m,
            restoreAfterError: k.restoreAfterError,
            mtype: k.mtype
        };
        switch (b) {
            case "edit":
                f.jqGrid("editRow", d, o), j.find("div.ui-inline-edit,div.ui-inline-del").hide(), j.find("div.ui-inline-save,div.ui-inline-cancel").show(), f.triggerHandler("jqGridAfterGridComplete");
                break;
            case "save":
                f.jqGrid("saveRow", d, o) && (j.find("div.ui-inline-edit,div.ui-inline-del").show(), j.find("div.ui-inline-save,div.ui-inline-cancel").hide(), f.triggerHandler("jqGridAfterGridComplete"));
                break;
            case "cancel":
                f.jqGrid("restoreRow", d, m), j.find("div.ui-inline-edit,div.ui-inline-del").show(), j.find("div.ui-inline-save,div.ui-inline-cancel").hide(), f.triggerHandler("jqGridAfterGridComplete");
                break;
            case "del":
                f.jqGrid("delGridRow", d, k.delOptions);
                break;
            case "formedit":
                f.jqGrid("setSelection", d), f.jqGrid("editGridRow", d, k.editOptions)
        }
    }, a.fn.fmatter.actions = function (b, c) {
        var
        d, e = {
            keys: !1,
            editbutton: !0,
            delbutton: !0,
            editformbutton: !1
        }, f = c.rowId,
            g = "",
            h = a.jgrid.getRegional(this, "nav"),
            i = a.jgrid.styleUI[c.styleUI || "jQueryUI"].fmatter,
            j = a.jgrid.styleUI[c.styleUI || "jQueryUI"].common;
        if (void
        0 !== c.colModel.formatoptions && (e = a.extend(e, c.colModel.formatoptions)), void
        0 === f || a.fmatter.isEmpty(f)) return "";
        var
        k = "onmouseover=jQuery(this).addClass('" + j.hover + "'); onmouseout=jQuery(this).removeClass('" + j.hover + "');  ";
        return e.editformbutton ? (d = "id='jEditButton_" + f + "' onclick=jQuery.fn.fmatter.rowactions.call(this,'formedit'); " + k, g += "<div title='" + h.edittitle + "' style='float:left;cursor:pointer;' class='ui-pg-div ui-inline-edit' " + d + "><span class='" + j.icon_base + " " + i.icon_edit + "'></span></div>") : e.editbutton && (d = "id='jEditButton_" + f + "' onclick=jQuery.fn.fmatter.rowactions.call(this,'edit'); " + k, g += "<div title='" + h.edittitle + "' style='float:left;cursor:pointer;' class='ui-pg-div ui-inline-edit' " + d + "><span class='" + j.icon_base + " " + i.icon_edit + "'></span></div>"), e.delbutton && (d = "id='jDeleteButton_" + f + "' onclick=jQuery.fn.fmatter.rowactions.call(this,'del'); " + k, g += "<div title='" + h.deltitle + "' style='float:left;' class='ui-pg-div ui-inline-del' " + d + "><span class='" + j.icon_base + " " + i.icon_del + "'></span></div>"), d = "id='jSaveButton_" + f + "' onclick=jQuery.fn.fmatter.rowactions.call(this,'save'); " + k, g += "<div title='" + h.savetitle + "' style='float:left;display:none' class='ui-pg-div ui-inline-save' " + d + "><span class='" + j.icon_base + " " + i.icon_save + "'></span></div>", d = "id='jCancelButton_" + f + "' onclick=jQuery.fn.fmatter.rowactions.call(this,'cancel'); " + k, "<div style='margin-left:8px;'>" + (g += "<div title='" + h.canceltitle + "' style='float:left;display:none;' class='ui-pg-div ui-inline-cancel' " + d + "><span class='" + j.icon_base + " " + i.icon_cancel + "'></span></div>") + "</div>"
    }, a.unformat = function (b, c, d, e) {
        var
        f, g, h = c.colModel.formatter,
            i = c.colModel.formatoptions || {}, j = /([\.\*\_\'\(\)\{\}\+\?\\])/g,
            k = c.colModel.unformat || a.fn.fmatter[h] && a.fn.fmatter[h].unformat;
        if (void
        0 !== k && a.isFunction(k)) f = k.call(this, a(b).text(), c, b);
        else if (void
        0 !== h && a.fmatter.isString(h)) {
            var
            l, m = a.jgrid.getRegional(this, "formatter") || {};
            switch (h) {
                case "integer":
                    i = a.extend({}, m.integer, i), g = i.thousandsSeparator.replace(j, "\\$1"), l = new
                    RegExp(g, "g"), f = a(b).text().replace(l, "");
                    break;
                case "number":
                    i = a.extend({}, m.number, i), g = i.thousandsSeparator.replace(j, "\\$1"), l = new
                    RegExp(g, "g"), f = a(b).text().replace(l, "").replace(i.decimalSeparator, ".");
                    break;
                case "currency":
                    i = a.extend({}, m.currency, i), g = i.thousandsSeparator.replace(j, "\\$1"), l = new
                    RegExp(g, "g"), f = a(b).text(), i.prefix && i.prefix.length && (f = f.substr(i.prefix.length)), i.suffix && i.suffix.length && (f = f.substr(0, f.length - i.suffix.length)), f = f.replace(l, "").replace(i.decimalSeparator, ".");
                    break;
                case "checkbox":
                    var
                    n = c.colModel.editoptions ? c.colModel.editoptions.value.split(":") : ["Yes", "No"];
                    f = a("input", b).is(":checked") ? n[0] : n[1];
                    break;
                case "select":
                    f = a.unformat.select(b, c, d, e);
                    break;
                case "actions":
                    return "";
                default:
                    f = a(b).text()
            }
        }
        return void
        0 !== f ? f : !0 === e ? a(b).text() : a.jgrid.htmlDecode(a(b).html())
    }, a.unformat.select = function (b, c, d, e) {
        var
        f = [],
            g = a(b).text();
        if (!0 === e) return g;
        var
        h = a.extend({}, void
        0 !== c.colModel.formatoptions ? c.colModel.formatoptions : c.colModel.editoptions),
            i = void
            0 === h.separator ? ":" : h.separator,
            j = void
            0 === h.delimiter ? ";" : h.delimiter;
        if (h.value) {
            var
            k, l = h.value,
                m = !0 === h.multiple,
                n = [];
            if (m && (n = g.split(","), n = a.map(n, function (b) {
                return a.trim(b)
            })), a.fmatter.isString(l)) {
                var
                o, p = l.split(j),
                    q = 0;
                for (o = 0; o < p.length; o++) if (k = p[o].split(i), k.length > 2 && (k[1] = a.map(k, function (a, b) {
                    if (b > 0) return a
                }).join(i)), m) a.inArray(a.trim(k[1]), n) > -1 && (f[q] = k[0], q++);
                else if (a.trim(k[1]) === a.trim(g)) {
                    f[0] = k[0];
                    break
                }
            } else(a.fmatter.isObject(l) || a.isArray(l)) && (m || (n[0] = g), f = a.map(n, function (b) {
                var
                c;
                if (a.each(l, function (a, d) {
                    if (d === b) return c = a, !1
                }), void
                0 !== c) return c
            }));
            return f.join(", ")
        }
        return g || ""
    }, a.unformat.date = function (b, c) {
        var
        d = a.jgrid.getRegional(this, "formatter.date") || {};
        return void
        0 !== c.formatoptions && (d = a.extend({}, d, c.formatoptions)), a.fmatter.isEmpty(b) ? a.fn.fmatter.defaultFormat(b, c) : a.jgrid.parseDate.call(this, d.newformat, b, d.srcformat, d)
    }
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "./jqModal", "./jqDnR"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.extend(a.jgrid, {
        showModal: function (a) {
            a.w.show()
        },
        closeModal: function (a) {
            a.w.hide().attr("aria-hidden", "true"), a.o && a.o.remove()
        },
        hideModal: function (b, c) {
            c = a.extend({
                jqm: !0,
                gb: "",
                removemodal: !1,
                formprop: !1,
                form: ""
            }, c || {});
            var
            d = !(!c.gb || "string" != typeof
            c.gb || "#gbox_" !== c.gb.substr(0, 6)) && a("#" + c.gb.substr(6))[0];
            if (c.onClose) {
                var
                e = d ? c.onClose.call(d, b) : c.onClose(b);
                if ("boolean" == typeof
                e && !e) return
            }
            if (c.formprop && d && c.form) {
                var
                f = a(b)[0].style.height,
                    g = a(b)[0].style.width;
                f.indexOf("px") > -1 && (f = parseFloat(f)), g.indexOf("px") > -1 && (g = parseFloat(g));
                var
                h, i;
                "edit" === c.form ? (h = "#" + a.jgrid.jqID("FrmGrid_" + c.gb.substr(6)), i = "formProp") : "view" === c.form && (h = "#" + a.jgrid.jqID("ViewGrid_" + c.gb.substr(6)), i = "viewProp"), a(d).data(i, {
                    top: parseFloat(a(b).css("top")),
                    left: parseFloat(a(b).css("left")),
                    width: g,
                    height: f,
                    dataheight: a(h).height(),
                    datawidth: a(h).width()
                })
            }
            if (a.fn.jqm && !0 === c.jqm) a(b).attr("aria-hidden", "true").jqmHide();
            else {
                if ("" !== c.gb) try {
                    a(".jqgrid-overlay:first", c.gb).hide()
                } catch (a) {}
                a(b).hide().attr("aria-hidden", "true")
            }
            c.removemodal && a(b).remove()
        },
        findPos: function (b) {
            var
            c = a(b).offset();
            return [c.left, c.top]
        },
        createModal: function (b, c, d, e, f, g, h) {
            d = a.extend(!0, {}, a.jgrid.jqModal || {}, d);
            var
            i = this,
                j = "rtl" === a(d.gbox).attr("dir"),
                k = a.jgrid.styleUI[d.styleUI || "jQueryUI"].modal,
                l = a.jgrid.styleUI[d.styleUI || "jQueryUI"].common,
                m = document.createElement("div");
            h = a.extend({}, h || {}), m.className = "ui-jqdialog " + k.modal, m.id = b.themodal;
            var
            n = document.createElement("div");
            n.className = "ui-jqdialog-titlebar " + k.header, n.id = b.modalhead, a(n).append("<span class='ui-jqdialog-title'>" + d.caption + "</span>");
            var
            o = a("<a class='ui-jqdialog-titlebar-close " + l.cornerall + "'></a>").hover(function () {
                o.addClass(l.hover)
            }, function () {
                o.removeClass(l.hover)
            }).append("<span class='" + l.icon_base + " " + k.icon_close + "'></span>");
            a(n).append(o), j ? (m.dir = "rtl", a(".ui-jqdialog-title", n).css("float", "right"), a(".ui-jqdialog-titlebar-close", n).css("left", "0.3em")) : (m.dir = "ltr", a(".ui-jqdialog-title", n).css("float", "left"), a(".ui-jqdialog-titlebar-close", n).css("right", "0.3em"));
            var
            p = document.createElement("div");
            a(p).addClass("ui-jqdialog-content " + k.content).attr("id", b.modalcontent), a(p).append(c), m.appendChild(p), a(m).prepend(n), !0 === g ? a("body").append(m) : "string" == typeof
            g ? a(g).append(m) : a(m).insertBefore(e), a(m).css(h), void
            0 === d.jqModal && (d.jqModal = !0);
            var
            q = {};
            if (a.fn.jqm && !0 === d.jqModal) {
                if (0 === d.left && 0 === d.top && d.overlay) {
                    var
                    r = [];
                    r = a.jgrid.findPos(f), d.left = r[0] + 4, d.top = r[1] + 4
                }
                q.top = d.top + "px", q.left = d.left
            } else 0 === d.left && 0 === d.top || (q.left = d.left, q.top = d.top + "px");
            if (a("a.ui-jqdialog-titlebar-close", n).click(function () {
                var
                c = a("#" + a.jgrid.jqID(b.themodal)).data("onClose") || d.onClose,
                    e = a("#" + a.jgrid.jqID(b.themodal)).data("gbox") || d.gbox;
                return i.hideModal("#" + a.jgrid.jqID(b.themodal), {
                    gb: e,
                    jqm: d.jqModal,
                    onClose: c,
                    removemodal: d.removemodal || !1,
                    formprop: !d.recreateForm || !1,
                    form: d.form || ""
                }), !1
            }), 0 !== d.width && d.width || (d.width = 300), 0 !== d.height && d.height || (d.height = 200), !d.zIndex) {
                var
                s = a(e).parents("*[role=dialog]").filter(":first").css("z-index");
                d.zIndex = s ? parseInt(s, 10) + 2 : 950
            }
            var
            t = 0;
            if (j && q.left && !g && (t = a(d.gbox).width() - (isNaN(d.width) ? 0 : parseInt(d.width, 10)) - 8, q.left = parseInt(q.left, 10) + parseInt(t, 10)), q.left && (q.left += "px"), a(m).css(a.extend({
                width: isNaN(d.width) ? "auto" : d.width + "px",
                height: isNaN(d.height) ? "auto" : d.height + "px",
                zIndex: d.zIndex,
                overflow: "hidden"
            }, q)).attr({
                tabIndex: "-1",
                role: "dialog",
                "aria-labelledby": b.modalhead,
                "aria-hidden": "true"
            }), void
            0 === d.drag && (d.drag = !0), void
            0 === d.resize && (d.resize = !0), d.drag) if (a(n).css("cursor", "move"), a.fn.tinyDraggable) a(m).tinyDraggable({
                handle: "#" + a.jgrid.jqID(n.id)
            });
            else try {
                a(m).draggable({
                    handle: a("#" + a.jgrid.jqID(n.id))
                })
            } catch (a) {}
            if (d.resize) if (a.fn.jqResize) a(m).append("<div class='jqResize " + k.resizable + " " + l.icon_base + " " + k.icon_resizable + "'></div>"), a("#" + a.jgrid.jqID(b.themodal)).jqResize(".jqResize", !! b.scrollelm && "#" + a.jgrid.jqID(b.scrollelm));
            else try {
                a(m).resizable({
                    handles: "se, sw",
                    alsoResize: !! b.scrollelm && "#" + a.jgrid.jqID(b.scrollelm)
                })
            } catch (a) {}!0 === d.closeOnEscape && a(m).keydown(function (c) {
                if (27 === c.which) {
                    var
                    e = a("#" + a.jgrid.jqID(b.themodal)).data("onClose") || d.onClose;
                    i.hideModal("#" + a.jgrid.jqID(b.themodal), {
                        gb: d.gbox,
                        jqm: d.jqModal,
                        onClose: e,
                        removemodal: d.removemodal || !1,
                        formprop: !d.recreateForm || !1,
                        form: d.form || ""
                    })
                }
            })
        },
        viewModal: function (b, c) {
            if (c = a.extend({
                toTop: !0,
                overlay: 10,
                modal: !1,
                overlayClass: "ui-widget-overlay",
                onShow: a.jgrid.showModal,
                onHide: a.jgrid.closeModal,
                gbox: "",
                jqm: !0,
                jqM: !0
            }, c || {}), void
            0 === c.focusField && (c.focusField = 0), "number" == typeof
            c.focusField && c.focusField >= 0 ? c.focusField = parseInt(c.focusField, 10) : "boolean" != typeof
            c.focusField || c.focusField ? c.focusField = 0 : c.focusField = !1, a.fn.jqm && !0 === c.jqm) c.jqM ? a(b).attr("aria-hidden", "false").jqm(c).jqmShow() : a(b).attr("aria-hidden", "false").jqmShow();
            else if ("" !== c.gbox && (a(".jqgrid-overlay:first", c.gbox).show(), a(b).data("gbox", c.gbox)), a(b).show().attr("aria-hidden", "false"), c.focusField >= 0) try {
                a(":input:visible", b)[c.focusField].focus()
            } catch (a) {}
        },
        info_dialog: function (b, c, d, e) {
            var
            f = {
                width: 290,
                height: "auto",
                dataheight: "auto",
                drag: !0,
                resize: !1,
                left: 250,
                top: 170,
                zIndex: 1e3,
                jqModal: !0,
                modal: !1,
                closeOnEscape: !0,
                align: "center",
                buttonalign: "center",
                buttons: []
            };
            a.extend(!0, f, a.jgrid.jqModal || {}, {
                caption: "<b>" + b + "</b>"
            }, e || {});
            var
            g = f.jqModal,
                h = this,
                i = a.jgrid.styleUI[f.styleUI || "jQueryUI"].modal,
                j = a.jgrid.styleUI[f.styleUI || "jQueryUI"].common;
            a.fn.jqm && !g && (g = !1);
            var
            k, l = "";
            if (f.buttons.length > 0) for (k = 0; k < f.buttons.length; k++) void
            0 === f.buttons[k].id && (f.buttons[k].id = "info_button_" + k), l += "<a id='" + f.buttons[k].id + "' class='fm-button " + j.button + "'>" + f.buttons[k].text + "</a>";
            var
            m = isNaN(f.dataheight) ? f.dataheight : f.dataheight + "px",
                n = "text-align:" + f.align + ";",
                o = "<div id='info_id'>";
            o += "<div id='infocnt' style='margin:0px;padding-bottom:1em;width:100%;overflow:auto;position:relative;height:" + m + ";" + n + "'>" + c + "</div>", o += d ? "<div class='" + i.content + "' style='text-align:" + f.buttonalign + ";padding-bottom:0.8em;padding-top:0.5em;background-image: none;border-width: 1px 0 0 0;'><a id='closedialog' class='fm-button " + j.button + "'>" + d + "</a>" + l + "</div>" : "" !== l ? "<div class='" + i.content + "' style='text-align:" + f.buttonalign + ";padding-bottom:0.8em;padding-top:0.5em;background-image: none;border-width: 1px 0 0 0;'>" + l + "</div>" : "", o += "</div>";
            try {
                "false" === a("#info_dialog").attr("aria-hidden") && a.jgrid.hideModal("#info_dialog", {
                    jqm: g
                }), a("#info_dialog").remove()
            } catch (a) {}
            a.jgrid.createModal({
                themodal: "info_dialog",
                modalhead: "info_head",
                modalcontent: "info_content",
                scrollelm: "infocnt"
            }, o, f, "", "", !0), l && a.each(f.buttons, function (b) {
                a("#" + a.jgrid.jqID(this.id), "#info_id").on("click", function () {
                    return f.buttons[b].onClick.call(a("#info_dialog")), !1
                })
            }), a("#closedialog", "#info_id").on("click", function () {
                return h.hideModal("#info_dialog", {
                    jqm: g,
                    onClose: a("#info_dialog").data("onClose") || f.onClose,
                    gb: a("#info_dialog").data("gbox") || f.gbox
                }), !1
            }), a(".fm-button", "#info_dialog").hover(function () {
                a(this).addClass(j.hover)
            }, function () {
                a(this).removeClass(j.hover)
            }), a.isFunction(f.beforeOpen) && f.beforeOpen(), a.jgrid.viewModal("#info_dialog", {
                onHide: function (a) {
                    a.w.hide().remove(), a.o && a.o.remove()
                },
                modal: f.modal,
                jqm: g
            }), a.isFunction(f.afterOpen) && f.afterOpen();
            try {
                a("#info_dialog").focus()
            } catch (a) {}
        },
        bindEv: function (b, c) {
            var
            d = this;
            a.isFunction(c.dataInit) && c.dataInit.call(d, b, c), c.dataEvents && a.each(c.dataEvents, function () {
                void
                0 !== this.data ? a(b).on(this.type, this.data, this.fn) : a(b).on(this.type, this.fn)
            })
        },
        createEl: function (b, c, d, e, f) {
            function
            g(b, c, d) {
                var
                e = ["dataInit", "dataEvents", "dataUrl", "buildSelect", "sopt", "searchhidden", "defaultValue", "attr", "custom_element", "custom_value", "oper"];
                e = e.concat(["cacheUrlData", "delimiter", "separator"]), void
                0 !== d && a.isArray(d) && a.merge(e, d), a.each(c, function (c, d) {
                    -1 === a.inArray(c, e) && a(b).attr(c, d)
                }), c.hasOwnProperty("id") || a(b).attr("id", a.jgrid.randId())
            }
            var
            h = "",
                i = this;
            switch (b) {
                case "textarea":
                    h = document.createElement("textarea"), e ? c.cols || a(h).css({
                        width: "98%"
                    }) : c.cols || (c.cols = 20), c.rows || (c.rows = 2), ("&nbsp;" === d || "&#160;" === d || 1 === d.length && 160 === d.charCodeAt(0)) && (d = ""), h.value = d, g(h, c), a(h).attr({
                        role: "textbox",
                        multiline: "true"
                    });
                    break;
                case "checkbox":
                    if (h = document.createElement("input"), h.type = "checkbox", c.value) {
                        var
                        j = c.value.split(":");
                        d === j[0] && (h.checked = !0, h.defaultChecked = !0), h.value = j[0], a(h).attr("offval", j[1])
                    } else {
                        var
                        k = (d + "").toLowerCase();
                        k.search(/(false|f|0|no|n|off|undefined)/i) < 0 && "" !== k ? (h.checked = !0, h.defaultChecked = !0, h.value = d) : h.value = "on", a(h).attr("offval", "off")
                    }
                    g(h, c, ["value"]), a(h).attr("role", "checkbox");
                    break;
                case "select":
                    h = document.createElement("select"), h.setAttribute("role", "select");
                    var
                    l, m = [];
                    if (!0 === c.multiple ? (l = !0, h.multiple = "multiple", a(h).attr("aria-multiselectable", "true")) : l = !1, null != c.dataUrl) {
                        var
                        n = null,
                            o = c.postData || f.postData;
                        try {
                            n = c.rowId
                        } catch (a) {}
                        i.p && i.p.idPrefix && (n = a.jgrid.stripPref(i.p.idPrefix, n)), a.ajax(a.extend({
                            url: a.isFunction(c.dataUrl) ? c.dataUrl.call(i, n, d, String(c.name)) : c.dataUrl,
                            type: "GET",
                            dataType: "html",
                            data: a.isFunction(o) ? o.call(i, n, d, String(c.name)) : o,
                            context: {
                                elem: h,
                                options: c,
                                vl: d
                            },
                            success: function (b) {
                                var
                                c, d = [],
                                    e = this.elem,
                                    f = this.vl,
                                    h = a.extend({}, this.options),
                                    j = !0 === h.multiple,
                                    k = !0 === h.cacheUrlData,
                                    l = "",
                                    m = a.isFunction(h.buildSelect) ? h.buildSelect.call(i, b) : b;
                                if ("string" == typeof
                                m && (m = a(a.trim(m)).html()), m) {
                                    if (a(e).append(m), g(e, h, o ? ["postData"] : void
                                    0), void
                                    0 === h.size && (h.size = j ? 3 : 1), j ? (d = f.split(","), d = a.map(d, function (b) {
                                        return a.trim(b)
                                    })) : d[0] = a.trim(f), a("option", e).each(function (b) {
                                        c = a(this).text(), f = a(this).val(), k && (l += (0 !== b ? ";" : "") + f + ":" + c), 0 === b && e.multiple && (this.selected = !1), a(this).attr("role", "option"), (a.inArray(a.trim(c), d) > -1 || a.inArray(a.trim(f), d) > -1) && (this.selected = "selected")
                                    }), k) if ("edit" === h.oper) a(i).jqGrid("setColProp", h.name, {
                                        editoptions: {
                                            buildSelect: null,
                                            dataUrl: null,
                                            value: l
                                        }
                                    });
                                    else if ("search" === h.oper) a(i).jqGrid("setColProp", h.name, {
                                        searchoptions: {
                                            dataUrl: null,
                                            value: l
                                        }
                                    });
                                    else if ("filter" === h.oper && a("#fbox_" + i.p.id)[0].p) {
                                        var
                                        n, p = a("#fbox_" + i.p.id)[0].p.columns;
                                        a.each(p, function (a) {
                                            if (n = this.index || this.name, h.name === n) return this.searchoptions.dataUrl = null, this.searchoptions.value = l, !1
                                        })
                                    }
                                    a(i).triggerHandler("jqGridAddEditAfterSelectUrlComplete", [e])
                                }
                            }
                        }, f || {}))
                    } else if (c.value) {
                        var
                        p;
                        void
                        0 === c.size && (c.size = l ? 3 : 1), l && (m = d.split(","), m = a.map(m, function (b) {
                            return a.trim(b)
                        })), "function" == typeof
                        c.value && (c.value = c.value());
                        var
                        q, r, s, t, u, v, w = void
                        0 === c.separator ? ":" : c.separator,
                            x = void
                            0 === c.delimiter ? ";" : c.delimiter;
                        if ("string" == typeof
                        c.value) for (q = c.value.split(x), p = 0; p < q.length; p++) r = q[p].split(w), r.length > 2 && (r[1] = a.map(r, function (a, b) {
                            if (b > 0) return a
                        }).join(w)), s = document.createElement("option"), s.setAttribute("role", "option"), s.value = r[0], s.innerHTML = r[1], h.appendChild(s), l || a.trim(r[0]) !== a.trim(d) && a.trim(r[1]) !== a.trim(d) || (s.selected = "selected"), l && (a.inArray(a.trim(r[1]), m) > -1 || a.inArray(a.trim(r[0]), m) > -1) && (s.selected = "selected");
                        else if ("[object Array]" === Object.prototype.toString.call(c.value)) for (t = c.value, p = 0; p < t.length; p++) 2 === t[p].length && (u = t[p][0], v = t[p][1], s = document.createElement("option"), s.setAttribute("role", "option"), s.value = u, s.innerHTML = v, h.appendChild(s), l || a.trim(u) !== a.trim(d) && a.trim(v) !== a.trim(d) || (s.selected = "selected"), l && (a.inArray(a.trim(v), m) > -1 || a.inArray(a.trim(u), m) > -1) && (s.selected = "selected"));
                        else if ("object" == typeof
                        c.value) {
                            t = c.value;
                            for (u in t) t.hasOwnProperty(u) && (s = document.createElement("option"), s.setAttribute("role", "option"), s.value = u, s.innerHTML = t[u], h.appendChild(s), l || a.trim(u) !== a.trim(d) && a.trim(t[u]) !== a.trim(d) || (s.selected = "selected"), l && (a.inArray(a.trim(t[u]), m) > -1 || a.inArray(a.trim(u), m) > -1) && (s.selected = "selected"))
                        }
                        g(h, c, ["value"])
                    }
                    break;
                case "image":
                case "file":
                    h = document.createElement("input"), h.type = b, g(h, c);
                    break;
                case "custom":
                    h = document.createElement("span");
                    try {
                        if (!a.isFunction(c.custom_element)) throw "e1";
                        var
                        y = c.custom_element.call(i, d, c);
                        if (!y) throw "e2";
                        y = a(y).addClass("customelement").attr({
                            id: c.id,
                            name: c.name
                        }), a(h).empty().append(y)
                    } catch (b) {
                        var
                        z = a.jgrid.getRegional(i, "errors"),
                            A = a.jgrid.getRegional(i, "edit");
                        "e1" === b ? a.jgrid.info_dialog(z.errcap, "function 'custom_element' " + A.msg.nodefined, A.bClose, {
                            styleUI: i.p.styleUI
                        }) : "e2" === b ? a.jgrid.info_dialog(z.errcap, "function 'custom_element' " + A.msg.novalue, A.bClose, {
                            styleUI: i.p.styleUI
                        }) : a.jgrid.info_dialog(z.errcap, "string" == typeof
                        b ? b : b.message, A.bClose, {
                            styleUI: i.p.styleUI
                        })
                    }
                    break;
                default:
                    var
                    B;
                    B = "button" === b ? "button" : "textbox", h = document.createElement("input"), h.type = b, h.value = d, g(h, c), "button" !== b && (e ? c.size || a(h).css({
                        width: "96%"
                    }) : c.size || (c.size = 20)), a(h).attr("role", B)
            }
            return h
        },
        checkDate: function (a, b) {
            var
            c, d = function (a) {
                return a % 4 != 0 || a % 100 == 0 && a % 400 != 0 ? 28 : 29
            }, e = {};
            if (a = a.toLowerCase(), c = -1 !== a.indexOf("/") ? "/" : -1 !== a.indexOf("-") ? "-" : -1 !== a.indexOf(".") ? "." : "/", a = a.split(c), b = b.split(c), 3 !== b.length) return !1;
            var
            f, g, h = -1,
                i = -1,
                j = -1;
            for (g = 0; g < a.length; g++) {
                var
                k = isNaN(b[g]) ? 0 : parseInt(b[g], 10);
                e[a[g]] = k, f = a[g], -1 !== f.indexOf("y") && (h = g), -1 !== f.indexOf("m") && (j = g), -1 !== f.indexOf("d") && (i = g)
            }
            f = "y" === a[h] || "yyyy" === a[h] ? 4 : "yy" === a[h] ? 2 : -1;
            var
            l, m = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
            return -1 !== h && (l = e[a[h]].toString(), 2 === f && 1 === l.length && (f = 1), l.length === f && (0 !== e[a[h]] || "00" === b[h]) && (-1 !== j && (l = e[a[j]].toString(), !(l.length < 1 || e[a[j]] < 1 || e[a[j]] > 12) && (-1 !== i && (l = e[a[i]].toString(), !(l.length < 1 || e[a[i]] < 1 || e[a[i]] > 31 || 2 === e[a[j]] && e[a[i]] > d(e[a[h]]) || e[a[i]] > m[e[a[j]]]))))))
        },
        isEmpty: function (a) {
            return !(void
            0 !== a && !a.match(/^\s+$/) && "" !== a)
        },
        checkTime: function (b) {
            var
            c, d = /^(\d{1,2}):(\d{2})([apAP][Mm])?$/;
            if (!a.jgrid.isEmpty(b)) {
                if (!(c = b.match(d))) return !1;
                if (c[3]) {
                    if (c[1] < 1 || c[1] > 12) return !1
                } else if (c[1] > 23) return !1;
                if (c[2] > 59) return !1
            }
            return !0
        },
        checkValues: function (b, c, d, e) {
            var
            f, g, h, i, j, k, l = this,
                m = l.p.colModel,
                n = a.jgrid.getRegional(this, "edit.msg");
            if (void
            0 === d) if ("string" == typeof
            c) {
                for (g = 0, j = m.length; g < j; g++) if (m[g].name === c) {
                    f = m[g].editrules, c = g, null != m[g].formoptions && (h = m[g].formoptions.label);
                    break
                }
            } else c >= 0 && (f = m[c].editrules);
            else f = d, h = void
            0 === e ? "_" : e;
            if (f) {
                if (h || (h = null != l.p.colNames ? l.p.colNames[c] : m[c].label), !0 === f.required && a.jgrid.isEmpty(b)) return [!1, h + ": " + n.required, ""];
                var
                o = !1 !== f.required;
                if (!0 === f.number && (!1 !== o || !a.jgrid.isEmpty(b)) && isNaN(b)) return [!1, h + ": " + n.number, ""];
                if (void
                0 !== f.minValue && !isNaN(f.minValue) && parseFloat(b) < parseFloat(f.minValue)) return [!1, h + ": " + n.minValue + " " + f.minValue, ""];
                if (void
                0 !== f.maxValue && !isNaN(f.maxValue) && parseFloat(b) > parseFloat(f.maxValue)) return [!1, h + ": " + n.maxValue + " " + f.maxValue, ""];
                var
                p;
                if (!0 === f.email && !(!1 === o && a.jgrid.isEmpty(b) || (p = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i, p.test(b)))) return [!1, h + ": " + n.email, ""];
                if (!0 === f.integer && (!1 !== o || !a.jgrid.isEmpty(b))) {
                    if (isNaN(b)) return [!1, h + ": " + n.integer, ""];
                    if (b % 1 != 0 || -1 !== b.indexOf(".")) return [!1, h + ": " + n.integer, ""]
                }
                if (!0 === f.date && !(!1 === o && a.jgrid.isEmpty(b) || (m[c].formatoptions && m[c].formatoptions.newformat ? (i = m[c].formatoptions.newformat, (k = a.jgrid.getRegional(l, "formatter.date.masks")) && k.hasOwnProperty(i) && (i = k[i])) : i = m[c].datefmt || "Y-m-d", a.jgrid.checkDate(i, b)))) return [!1, h + ": " + n.date + " - " + i, ""];
                if (!0 === f.time && !(!1 === o && a.jgrid.isEmpty(b) || a.jgrid.checkTime(b))) return [!1, h + ": " + n.date + " - hh:mm (am/pm)", ""];
                if (!0 === f.url && !(!1 === o && a.jgrid.isEmpty(b) || (p = /^(((https?)|(ftp)):\/\/([\-\w]+\.)+\w{2,3}(\/[%\-\w]+(\.\w{2,})?)*(([\w\-\.\?\\\/+@&#;`~=%!]*)(\.\w{2,})?)*\/?)/i, p.test(b)))) return [!1, h + ": " + n.url, ""];
                if (!0 === f.custom && (!1 !== o || !a.jgrid.isEmpty(b))) {
                    if (a.isFunction(f.custom_func)) {
                        var
                        q = f.custom_func.call(l, b, h, c);
                        return a.isArray(q) ? q : [!1, n.customarray, ""]
                    }
                    return [!1, n.customfcheck, ""]
                }
            }
            return [!0, "", ""]
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "./grid.common"], a) : a(jQuery)
}(function (a) {
    "use strict";
    var
    b = {};
    a.jgrid.extend({
        editGridRow: function (c, d) {
            var
            e = a.jgrid.getRegional(this[0], "edit"),
                f = this[0].p.styleUI,
                g = a.jgrid.styleUI[f].formedit,
                h = a.jgrid.styleUI[f].common;
            return d = a.extend(!0, {
                top: 0,
                left: 0,
                width: "500",
                datawidth: "auto",
                height: "auto",
                dataheight: "auto",
                modal: !1,
                overlay: 30,
                drag: !0,
                resize: !0,
                url: null,
                mtype: "POST",
                clearAfterAdd: !0,
                closeAfterEdit: !1,
                reloadAfterSubmit: !0,
                onInitializeForm: null,
                beforeInitData: null,
                beforeShowForm: null,
                afterShowForm: null,
                beforeSubmit: null,
                afterSubmit: null,
                onclickSubmit: null,
                afterComplete: null,
                onclickPgButtons: null,
                afterclickPgButtons: null,
                editData: {},
                recreateForm: !1,
                jqModal: !0,
                closeOnEscape: !1,
                addedrow: "first",
                topinfo: "",
                bottominfo: "",
                saveicon: [],
                closeicon: [],
                savekey: [!1, 13],
                navkeys: [!1, 38, 40],
                checkOnSubmit: !1,
                checkOnUpdate: !1,
                processing: !1,
                onClose: null,
                ajaxEditOptions: {},
                serializeEditData: null,
                viewPagerButtons: !0,
                overlayClass: h.overlay,
                removemodal: !0,
                form: "edit",
                template: null,
                focusField: !0,
                editselected: !1
            }, e, d || {}), b[a(this)[0].p.id] = d, this.each(function () {
                function
                e() {
                    var
                    c, d = {};
                    a(A).find(".FormElement").each(function () {
                        var
                        c = a(".customelement", this);
                        if (c.length) {
                            var
                            e = c[0],
                                f = a(e).attr("name");
                            a.each(s.p.colModel, function () {
                                if (this.name === f && this.editoptions && a.isFunction(this.editoptions.custom_value)) {
                                    try {
                                        if (u[f] = this.editoptions.custom_value.call(s, a("#" + a.jgrid.jqID(f), A), "get"), void
                                        0 === u[f]) throw "e1"
                                    } catch (c) {
                                        "e1" === c ? a.jgrid.info_dialog(G.errcap, "function 'custom_value' " + b[a(this)[0]].p.msg.novalue, b[a(this)[0]].p.bClose, {
                                            styleUI: b[a(this)[0]].p.styleUI
                                        }) : a.jgrid.info_dialog(G.errcap, c.message, b[a(this)[0]].p.bClose, {
                                            styleUI: b[a(this)[0]].p.styleUI
                                        })
                                    }
                                    return !0
                                }
                            })
                        } else {
                            switch (a(this).get(0).type) {
                                case "checkbox":
                                    if (a(this).is(":checked")) u[this.name] = a(this).val();
                                    else {
                                        var
                                        g = a(this).attr("offval");
                                        u[this.name] = g
                                    }
                                    break;
                                case "select-one":
                                    u[this.name] = a(this).val();
                                    break;
                                case "select-multiple":
                                    u[this.name] = a(this).val(), u[this.name] = u[this.name] ? u[this.name].join(",") : "";
                                    break;
                                case "password":
                                case "text":
                                case "textarea":
                                case "button":
                                    u[this.name] = a(this).val();
                                    break;
                                case "radio":
                                    if (d.hasOwnProperty(this.name)) return !0;
                                    d[this.name] = void
                                    0 === a(this).attr("offval") ? "off" : a(this).attr("offval")
                            }
                            s.p.autoencode && (u[this.name] = a.jgrid.htmlEncode(u[this.name]))
                        }
                    });
                    for (c in d) if (d.hasOwnProperty(c)) {
                        var
                        e = a('input[name="' + c + '"]:checked', A).val();
                        u[c] = void
                        0 !== e ? e : d[c], s.p.autoencode && (u[c] = a.jgrid.htmlEncode(u[c]))
                    }
                    return !0
                }

                function
                f(c, d, e, f) {
                    var
                    h, i, j, k, l, m, n, o, p = 0,
                        q = [],
                        r = !1,
                        t = "<td class='CaptionTD'>&#160;</td><td class='DataTD'>&#160;</td>",
                        u = "";
                    for (n = 1; n <= f; n++) u += t;
                    if ("_empty" !== c && (r = a(d).jqGrid("getInd", c)), a(d.p.colModel).each(function (n) {
                        if (h = this.name, i = (!this.editrules || !0 !== this.editrules.edithidden) && !0 === this.hidden, l = i ? "style='display:none'" : "", "cb" !== h && "subgrid" !== h && !0 === this.editable && "rn" !== h) {
                            if (!1 === r) k = "";
                            else if (h === d.p.ExpandColumn && !0 === d.p.treeGrid) k = a("td[role='gridcell']:eq(" + n + ")", d.rows[r]).text();
                            else {
                                try {
                                    k = a.unformat.call(d, a("td[role='gridcell']:eq(" + n + ")", d.rows[r]), {
                                        rowId: c,
                                        colModel: this
                                    }, n)
                                } catch (b) {
                                    k = this.edittype && "textarea" === this.edittype ? a("td[role='gridcell']:eq(" + n + ")", d.rows[r]).text() : a("td[role='gridcell']:eq(" + n + ")", d.rows[r]).html()
                                }(!k || "&nbsp;" === k || "&#160;" === k || 1 === k.length && 160 === k.charCodeAt(0)) && (k = "")
                            }
                            var
                            t = a.extend({}, this.editoptions || {}, {
                                id: h,
                                name: h,
                                rowId: c,
                                oper: "edit"
                            }),
                                v = a.extend({}, {
                                    elmprefix: "",
                                    elmsuffix: "",
                                    rowabove: !1,
                                    rowcontent: ""
                                }, this.formoptions || {}),
                                w = parseInt(v.rowpos, 10) || p + 1,
                                x = parseInt(2 * (parseInt(v.colpos, 10) || 1), 10);
                            if ("_empty" === c && t.defaultValue && (k = a.isFunction(t.defaultValue) ? t.defaultValue.call(s) : t.defaultValue), this.edittype || (this.edittype = "text"), s.p.autoencode && (k = a.jgrid.htmlDecode(k)), m = a.jgrid.createEl.call(s, this.edittype, t, k, !1, a.extend({}, a.jgrid.ajaxOptions, d.p.ajaxSelectOptions || {})), "select" === this.edittype && (k = a(m).val(), "select-multiple" === a(m).get(0).type && k && (k = k.join(","))), "checkbox" === this.edittype && (k = a(m).is(":checked") ? a(m).val() : a(m).attr("offval")), a(m).addClass("FormElement"), a.inArray(this.edittype, ["text", "textarea", "password", "select"]) > -1 && a(m).addClass(g.inputClass), o = !0, F) {
                                var
                                z = a(L).find("#" + h);
                                z.length ? z.replaceWith(m) : o = !1
                            } else {
                                if (j = a(e).find("tr[rowpos=" + w + "]"), v.rowabove) {
                                    var
                                    A = a("<tr><td class='contentinfo' colspan='" + 2 * f + "'>" + v.rowcontent + "</td></tr>");
                                    a(e).append(A), A[0].rp = w
                                }
                                0 === j.length && (j = a("<tr " + l + " rowpos='" + w + "'></tr>").addClass("FormData").attr("id", "tr_" + h), a(j).append(u), a(e).append(j), j[0].rp = w), a("td:eq(" + (x - 2) + ")", j[0]).html("<label for='" + h + "'>" + (void
                                0 === v.label ? d.p.colNames[n] : v.label) + "</label>"), a("td:eq(" + (x - 1) + ")", j[0]).append(v.elmprefix).append(m).append(v.elmsuffix)
                            }(b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && o && (s.p.savedData[h] = k), "custom" === this.edittype && a.isFunction(t.custom_value) && t.custom_value.call(s, a("#" + h, y), "set", k), a.jgrid.bindEv.call(s, m, t), q[p] = n, p++
                        }
                    }), p > 0) {
                        var
                        v;
                        F ? (v = "<div class='FormData' style='display:none'><input class='FormElement' id='id_g' type='text' name='" + d.p.id + "_id' value='" + c + "'/>", a(L).append(v)) : (v = a("<tr class='FormData' style='display:none'><td class='CaptionTD'></td><td colspan='" + (2 * f - 1) + "' class='DataTD'><input class='FormElement' id='id_g' type='text' name='" + d.p.id + "_id' value='" + c + "'/></td></tr>"), v[0].rp = p + 999, a(e).append(v)), (b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (s.p.savedData[d.p.id + "_id"] = c)
                    }
                    return q
                }

                function
                i(c, d, e) {
                    var
                    f, g, h, i, j, k, l = 0;
                    (b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (s.p.savedData = {}, s.p.savedData[d.p.id + "_id"] = c);
                    var
                    m = d.p.colModel;
                    if ("_empty" === c) return a(m).each(function () {
                        f = this.name, i = a.extend({}, this.editoptions || {}), (h = a("#" + a.jgrid.jqID(f), e)) && h.length && null !== h[0] && (j = "", "custom" === this.edittype && a.isFunction(i.custom_value) ? i.custom_value.call(s, a("#" + f, e), "set", j) : i.defaultValue ? (j = a.isFunction(i.defaultValue) ? i.defaultValue.call(s) : i.defaultValue, "checkbox" === h[0].type ? (k = j.toLowerCase(), k.search(/(false|f|0|no|n|off|undefined)/i) < 0 && "" !== k ? (h[0].checked = !0, h[0].defaultChecked = !0, h[0].value = j) : (h[0].checked = !1, h[0].defaultChecked = !1)) : h.val(j)) : "checkbox" === h[0].type ? (h[0].checked = !1, h[0].defaultChecked = !1, j = a(h).attr("offval")) : h[0].type && "select" === h[0].type.substr(0, 6) ? h[0].selectedIndex = 0 : h.val(j), (!0 === b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (s.p.savedData[f] = j))
                    }), void
                    a("#id_g", e).val(c);
                    var
                    n = a(d).jqGrid("getInd", c, !0);
                    n && (a('td[role="gridcell"]', n).each(function (h) {
                        if ("cb" !== (f = m[h].name) && "subgrid" !== f && "rn" !== f && !0 === m[h].editable) {
                            if (f === d.p.ExpandColumn && !0 === d.p.treeGrid) g = a(this).text();
                            else try {
                                g = a.unformat.call(d, a(this), {
                                    rowId: c,
                                    colModel: m[h]
                                }, h)
                            } catch (b) {
                                g = "textarea" === m[h].edittype ? a(this).text() : a(this).html()
                            }
                            switch (s.p.autoencode && (g = a.jgrid.htmlDecode(g)), (!0 === b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (s.p.savedData[f] = g), f = a.jgrid.jqID(f), m[h].edittype) {
                                case "password":
                                case "text":
                                case "button":
                                case "image":
                                case "textarea":
                                    ("&nbsp;" === g || "&#160;" === g || 1 === g.length && 160 === g.charCodeAt(0)) && (g = ""), a("#" + f, e).val(g);
                                    break;
                                case "select":
                                    var
                                    i = g.split(",");
                                    i = a.map(i, function (b) {
                                        return a.trim(b)
                                    }), a("#" + f + " option", e).each(function () {
                                        m[h].editoptions.multiple || a.trim(g) !== a.trim(a(this).text()) && i[0] !== a.trim(a(this).text()) && i[0] !== a.trim(a(this).val()) ? m[h].editoptions.multiple && (a.inArray(a.trim(a(this).text()), i) > -1 || a.inArray(a.trim(a(this).val()), i) > -1) ? this.selected = !0 : this.selected = !1 : this.selected = !0
                                    }), (!0 === b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (g = a("#" + f, e).val(), m[h].editoptions.multiple && (g = g.join(",")), s.p.savedData[f] = g);
                                    break;
                                case "checkbox":
                                    if (g = String(g), m[h].editoptions && m[h].editoptions.value) {
                                        m[h].editoptions.value.split(":")[0] === g ? a("#" + f, e)[s.p.useProp ? "prop" : "attr"]({
                                            checked: !0,
                                            defaultChecked: !0
                                        }) : a("#" + f, e)[s.p.useProp ? "prop" : "attr"]({
                                            checked: !1,
                                            defaultChecked: !1
                                        })
                                    } else g = g.toLowerCase(), g.search(/(false|f|0|no|n|off|undefined)/i) < 0 && "" !== g ? (a("#" + f, e)[s.p.useProp ? "prop" : "attr"]("checked", !0), a("#" + f, e)[s.p.useProp ? "prop" : "attr"]("defaultChecked", !0)) : (a("#" + f, e)[s.p.useProp ? "prop" : "attr"]("checked", !1), a("#" + f, e)[s.p.useProp ? "prop" : "attr"]("defaultChecked", !1));
                                    (!0 === b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (g = a("#" + f, e).is(":checked") ? a("#" + f, e).val() : a("#" + f, e).attr("offval"), s.p.savedData[f] = g);
                                    break;
                                case "custom":
                                    try {
                                        if (!m[h].editoptions || !a.isFunction(m[h].editoptions.custom_value)) throw "e1";
                                        m[h].editoptions.custom_value.call(s, a("#" + f, e), "set", g)
                                    } catch (c) {
                                        "e1" === c ? a.jgrid.info_dialog(G.errcap, "function 'custom_value' " + b[a(this)[0]].p.msg.nodefined, a.rp_ge[a(this)[0]].p.bClose, {
                                            styleUI: b[a(this)[0]].p.styleUI
                                        }) : a.jgrid.info_dialog(G.errcap, c.message, a.rp_ge[a(this)[0]].p.bClose, {
                                            styleUI: b[a(this)[0]].p.styleUI
                                        })
                                    }
                            }
                            l++
                        }
                    }), l > 0 && (a("#id_g", A).val(c), (!0 === b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (s.p.savedData[d.p.id + "_id"] = c)))
                }

                function
                j() {
                    a.each(s.p.colModel, function (a, b) {
                        b.editoptions && !0 === b.editoptions.NullIfEmpty && u.hasOwnProperty(b.name) && "" === u[b.name] && (u[b.name] = "null")
                    })
                }

                function
                k() {
                    var
                    c, e, f, g, k, l, m, n = [!0, "", ""],
                        o = {}, p = s.p.prmNames,
                        q = a(s).triggerHandler("jqGridAddEditBeforeCheckValues", [u, a(y), w]);
                    q && "object" == typeof
                    q && (u = q), a.isFunction(b[s.p.id].beforeCheckValues) && (q = b[s.p.id].beforeCheckValues.call(s, u, a(y), w)) && "object" == typeof
                    q && (u = q);
                    for (g in u) if (u.hasOwnProperty(g) && (n = a.jgrid.checkValues.call(s, u[g], g), !1 === n[0])) break;
                    if (j(), n[0] && (o = a(s).triggerHandler("jqGridAddEditClickSubmit", [b[s.p.id], u, w]), void
                    0 === o && a.isFunction(b[s.p.id].onclickSubmit) && (o = b[s.p.id].onclickSubmit.call(s, b[s.p.id], u, w) || {}), n = a(s).triggerHandler("jqGridAddEditBeforeSubmit", [u, a(y), w]), void
                    0 === n && (n = [!0, "", ""]), n[0] && a.isFunction(b[s.p.id].beforeSubmit) && (n = b[s.p.id].beforeSubmit.call(s, u, a(y), w))), n[0] && !b[s.p.id].processing) {
                        if (b[s.p.id].processing = !0, a("#sData", A + "_2").addClass(h.active), m = b[s.p.id].url || a(s).jqGrid("getGridParam", "editurl"), f = p.oper, e = "clientArray" === m ? s.p.keyName : p.id, u[f] = "_empty" === a.trim(u[s.p.id + "_id"]) ? p.addoper : p.editoper, u[f] !== p.addoper ? u[e] = u[s.p.id + "_id"] : void
                        0 === u[e] && (u[e] = u[s.p.id + "_id"]), delete
                        u[s.p.id + "_id"], u = a.extend(u, b[s.p.id].editData, o), !0 === s.p.treeGrid) {
                            if (u[f] === p.addoper) {
                                k = a(s).jqGrid("getGridParam", "selrow");
                                var
                                r = "adjacency" === s.p.treeGridModel ? s.p.treeReader.parent_id_field : "parent_id";
                                u[r] = k
                            }
                            for (l in s.p.treeReader) if (s.p.treeReader.hasOwnProperty(l)) {
                                var
                                t = s.p.treeReader[l];
                                if (u.hasOwnProperty(t)) {
                                    if (u[f] === p.addoper && "parent_id_field" === l) continue;
                                    delete
                                    u[t]
                                }
                            }
                        }
                        u[e] = a.jgrid.stripPref(s.p.idPrefix, u[e]);
                        var
                        v = a.extend({
                            url: m,
                            type: b[s.p.id].mtype,
                            data: a.isFunction(b[s.p.id].serializeEditData) ? b[s.p.id].serializeEditData.call(s, u) : u,
                            complete: function (g, j) {
                                var
                                l;
                                if (a("#sData", A + "_2").removeClass(h.active), u[e] = s.p.idPrefix + u[e], g.status >= 300 && 304 !== g.status ? (n[0] = !1, n[1] = a(s).triggerHandler("jqGridAddEditErrorTextFormat", [g, w]), a.isFunction(b[s.p.id].errorTextFormat) ? n[1] = b[s.p.id].errorTextFormat.call(s, g, w) : n[1] = j + " Status: '" + g.statusText + "'. Error code: " + g.status) : (n = a(s).triggerHandler("jqGridAddEditAfterSubmit", [g, u, w]), void
                                0 === n && (n = [!0, "", ""]), n[0] && a.isFunction(b[s.p.id].afterSubmit) && (n = b[s.p.id].afterSubmit.call(s, g, u, w))), !1 === n[0]) a(".FormError", y).html(n[1]), a(".FormError", y).show();
                                else if (s.p.autoencode && a.each(u, function (b, c) {
                                    u[b] = a.jgrid.htmlDecode(c)
                                }), u[f] === p.addoper ? (n[2] || (n[2] = a.jgrid.randId()), null == u[e] || "_empty" === u[e] || "" === u[e] ? u[e] = n[2] : n[2] = u[e], b[s.p.id].reloadAfterSubmit ? a(s).trigger("reloadGrid") : !0 === s.p.treeGrid ? a(s).jqGrid("addChildNode", n[2], k, u) : a(s).jqGrid("addRowData", n[2], u, d.addedrow), b[s.p.id].closeAfterAdd ? (!0 !== s.p.treeGrid && a(s).jqGrid("setSelection", n[2]), a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                    gb: "#gbox_" + a.jgrid.jqID(x),
                                    jqm: d.jqModal,
                                    onClose: b[s.p.id].onClose,
                                    removemodal: b[s.p.id].removemodal,
                                    formprop: !b[s.p.id].recreateForm,
                                    form: b[s.p.id].form
                                })) : b[s.p.id].clearAfterAdd && i("_empty", s, y)) : (b[s.p.id].reloadAfterSubmit ? (a(s).trigger("reloadGrid"), b[s.p.id].closeAfterEdit || setTimeout(function () {
                                    a(s).jqGrid("setSelection", u[e])
                                }, 1e3)) : !0 === s.p.treeGrid ? a(s).jqGrid("setTreeRow", u[e], u) : a(s).jqGrid("setRowData", u[e], u), b[s.p.id].closeAfterEdit && a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                    gb: "#gbox_" + a.jgrid.jqID(x),
                                    jqm: d.jqModal,
                                    onClose: b[s.p.id].onClose,
                                    removemodal: b[s.p.id].removemodal,
                                    formprop: !b[s.p.id].recreateForm,
                                    form: b[s.p.id].form
                                })), (a.isFunction(b[s.p.id].afterComplete) || a._data(a(s)[0], "events").hasOwnProperty("jqGridAddEditAfterComplete")) && (c = g, setTimeout(function () {
                                    a(s).triggerHandler("jqGridAddEditAfterComplete", [c, u, a(y), w]);
                                    try {
                                        b[s.p.id].afterComplete.call(s, c, u, a(y), w)
                                    } catch (a) {}
                                    c = null
                                }, 500)), (b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) && (a(y).data("disabled", !1), "_empty" !== s.p.savedData[s.p.id + "_id"])) for (l in s.p.savedData) s.p.savedData.hasOwnProperty(l) && u[l] && (s.p.savedData[l] = u[l]);
                                b[s.p.id].processing = !1;
                                try {
                                    a(":input:visible", y)[0].focus()
                                } catch (a) {}
                            }
                        }, a.jgrid.ajaxOptions, b[s.p.id].ajaxEditOptions);
                        if (v.url || b[s.p.id].useDataProxy || (a.isFunction(s.p.dataProxy) ? b[s.p.id].useDataProxy = !0 : (n[0] = !1, n[1] += " " + G.nourl)), n[0]) if (b[s.p.id].useDataProxy) {
                            var
                            z = s.p.dataProxy.call(s, v, "set_" + s.p.id);
                            void
                            0 === z && (z = [!0, ""]), !1 === z[0] ? (n[0] = !1, n[1] = z[1] || "Error deleting the selected row!") : (v.data.oper === p.addoper && b[s.p.id].closeAfterAdd && a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(x),
                                jqm: d.jqModal,
                                onClose: b[s.p.id].onClose,
                                removemodal: b[s.p.id].removemodal,
                                formprop: !b[s.p.id].recreateForm,
                                form: b[s.p.id].form
                            }), v.data.oper === p.editoper && b[s.p.id].closeAfterEdit && a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(x),
                                jqm: d.jqModal,
                                onClose: b[s.p.id].onClose,
                                removemodal: b[s.p.id].removemodal,
                                formprop: !b[s.p.id].recreateForm,
                                form: b[s.p.id].form
                            }))
                        } else "clientArray" === v.url ? (b[s.p.id].reloadAfterSubmit = !1, u = v.data, v.complete({
                            status: 200,
                            statusText: ""
                        }, "")) : a.ajax(v)
                    }!1 === n[0] && (a(".FormError", y).html(n[1]), a(".FormError", y).show())
                }

                function
                l(b, c) {
                    var
                    d, e = !1;
                    if (!(e = !(a.isPlainObject(b) && a.isPlainObject(c) && Object.getOwnPropertyNames(b).length === Object.getOwnPropertyNames(c).length))) for (d in c) if (c.hasOwnProperty(d)) {
                        if (!b.hasOwnProperty(d)) {
                            e = !0;
                            break
                        }
                        if (b[d] !== c[d]) {
                            e = !0;
                            break
                        }
                    }
                    return e
                }

                function
                m() {
                    var
                    c = !0;
                    return a(".FormError", y).hide(), b[s.p.id].checkOnUpdate && (u = {}, e(), (v = l(u, s.p.savedData)) && (a(y).data("disabled", !0), a(".confirm", "#" + B.themodal).show(), c = !1)), c
                }

                function
                n() {
                    var
                    b;
                    if ("_empty" !== c && void
                    0 !== s.p.savedRow && s.p.savedRow.length > 0 && a.isFunction(a.fn.jqGrid.restoreRow)) for (b = 0; b < s.p.savedRow.length; b++) if (s.p.savedRow[b].id === c) {
                        a(s).jqGrid("restoreRow", c);
                        break
                    }
                }

                function
                o(b, c) {
                    var
                    d = c[1].length - 1;
                    0 === b ? a("#pData", t).addClass(h.disabled) : void
                    0 !== c[1][b - 1] && a("#" + a.jgrid.jqID(c[1][b - 1])).hasClass(h.disabled) ? a("#pData", t).addClass(h.disabled) : a("#pData", t).removeClass(h.disabled), b === d ? a("#nData", t).addClass(h.disabled) : void
                    0 !== c[1][b + 1] && a("#" + a.jgrid.jqID(c[1][b + 1])).hasClass(h.disabled) ? a("#nData", t).addClass(h.disabled) : a("#nData", t).removeClass(h.disabled)
                }

                function
                p() {
                    var
                    c, d = a(s).jqGrid("getDataIDs"),
                        e = a("#id_g", A).val();
                    if (s.p.multiselect && b[s.p.id].editselected) {
                        for (var
                        f = [], g = 0, h = d.length; g < h; g++) - 1 !== a.inArray(d[g], s.p.selarrrow) && f.push(d[g]);
                        return c = a.inArray(e, f), [c, f]
                    }
                    return c = a.inArray(e, d), [c, d]
                }

                function
                q(a) {
                    var
                    b = "";
                    return "string" == typeof
                    a && (b = a.replace(/\{([\w\-]+)(?:\:([\w\.]*)(?:\((.*?)?\))?)?\}/g, function (a, b) {
                        return '<span id="' + b + '" ></span>'
                    })), b
                }

                function
                r() {
                    if (b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) {
                        var
                        c = [],
                            d = {};
                        c = a.map(s.p.savedData, function (a, b) {
                            return b
                        }), a(".FormElement", L).each(function () {
                            if (-1 === c.indexOf(this.name)) {
                                var
                                b = a(this).val(),
                                    e = a(this).get(0).type;
                                if ("checkbox" === e) a(this).is(":checked") || (b = a(this).attr("offval"));
                                else if ("select-multiple" === e) b = b.join(",");
                                else if ("radio" === e) {
                                    if (d.hasOwnProperty(this.name)) return !0;
                                    d[this.name] = void
                                    0 === a(this).attr("offval") ? "off" : a(this).attr("offval")
                                }
                                s.p.savedData[this.name] = b
                            }
                        });
                        for (var
                        e in d) if (d.hasOwnProperty(e)) {
                            var
                            f = a('input[name="' + e + '"]:checked', L).val();
                            s.p.savedData[e] = void
                            0 !== f ? f : d[e]
                        }
                    }
                }
                var
                s = this;
                if (s.grid && c) {
                    s.p.savedData = {};
                    var
                    t, u, v, w, x = s.p.id,
                        y = "FrmGrid_" + x,
                        z = "TblGrid_" + x,
                        A = "#" + a.jgrid.jqID(z),
                        B = {
                            themodal: "editmod" + x,
                            modalhead: "edithd" + x,
                            modalcontent: "editcnt" + x,
                            scrollelm: y
                        }, C = !0,
                        D = 1,
                        E = 0,
                        F = "string" == typeof
                        b[s.p.id].template && b[s.p.id].template.length > 0,
                        G = a.jgrid.getRegional(this, "errors");
                    b[s.p.id].styleUI = s.p.styleUI || "jQueryUI", a.jgrid.isMobile() && (b[s.p.id].resize = !1), "new" === c ? (c = "_empty", w = "add", d.caption = b[s.p.id].addCaption) : (d.caption = b[s.p.id].editCaption, w = "edit"), d.recreateForm || a(s).data("formProp") && a.extend(b[a(this)[0].p.id], a(s).data("formProp"));
                    var
                    H = !0;
                    d.checkOnUpdate && d.jqModal && !d.modal && (H = !1);
                    var
                    I, J = isNaN(b[a(this)[0].p.id].dataheight) ? b[a(this)[0].p.id].dataheight : b[a(this)[0].p.id].dataheight + "px",
                        K = isNaN(b[a(this)[0].p.id].datawidth) ? b[a(this)[0].p.id].datawidth : b[a(this)[0].p.id].datawidth + "px",
                        L = a("<form name='FormPost' id='" + y + "' class='FormGrid' onSubmit='return false;' style='width:" + K + ";height:" + J + ";'></form>").data("disabled", !1);
                    if (F ? (I = q(b[a(this)[0].p.id].template), t = A) : (I = a("<table id='" + z + "' class='EditTable ui-common-table'><tbody></tbody></table>"), t = A + "_2"), y = "#" + a.jgrid.jqID(y), a(L).append("<div class='FormError " + h.error + "' style='display:none;'></div>"), a(L).append("<div class='tinfo topinfo'>" + b[s.p.id].topinfo + "</div>"), a(s.p.colModel).each(function () {
                        var
                        a = this.formoptions;
                        D = Math.max(D, a ? a.colpos || 0 : 0), E = Math.max(E, a ? a.rowpos || 0 : 0)
                    }), a(L).append(I), C = a(s).triggerHandler("jqGridAddEditBeforeInitData", [L, w]), void
                    0 === C && (C = !0), C && a.isFunction(b[s.p.id].beforeInitData) && (C = b[s.p.id].beforeInitData.call(s, L, w)), !1 !== C) {
                        n(), f(c, s, I, D);
                        var
                        M = "rtl" === s.p.direction,
                            N = M ? "nData" : "pData",
                            O = M ? "pData" : "nData",
                            P = "<a id='" + N + "' class='fm-button " + h.button + "'><span class='" + h.icon_base + " " + g.icon_prev + "'></span></a>",
                            Q = "<a id='" + O + "' class='fm-button " + h.button + "'><span class='" + h.icon_base + " " + g.icon_next + "'></span></a>",
                            R = "<a id='sData' class='fm-button " + h.button + "'>" + d.bSubmit + "</a>",
                            S = "<a id='cData' class='fm-button " + h.button + "'>" + d.bCancel + "</a>",
                            T = "<table style='height:auto' class='EditTable ui-common-table' id='" + z + "_2'><tbody><tr><td colspan='2'><hr class='" + h.content + "' style='margin:1px'/></td></tr><tr id='Act_Buttons'><td class='navButton'>" + (M ? Q + P : P + Q) + "</td><td class='EditButton'>" + R + S + "</td></tr>";
                        if (T += "</tbody></table>", E > 0) {
                            var
                            U = [];
                            a.each(a(I)[0].rows, function (a, b) {
                                U[a] = b
                            }), U.sort(function (a, b) {
                                return a.rp > b.rp ? 1 : a.rp < b.rp ? -1 : 0
                            }), a.each(U, function (b, c) {
                                a("tbody", I).append(c)
                            })
                        }
                        d.gbox = "#gbox_" + a.jgrid.jqID(x);
                        var
                        V = !1;
                        !0 === d.closeOnEscape && (d.closeOnEscape = !1, V = !0);
                        var
                        W;
                        if (F ? (a(L).find("#pData").replaceWith(P), a(L).find("#nData").replaceWith(Q), a(L).find("#sData").replaceWith(R), a(L).find("#cData").replaceWith(S), W = a("<div id=" + z + "></div>").append(L)) : W = a("<div></div>").append(L).append(T), a(L).append("<div class='binfo topinfo bottominfo'>" + b[s.p.id].bottominfo + "</div>"), a.jgrid.createModal(B, W, b[a(this)[0].p.id], "#gview_" + a.jgrid.jqID(s.p.id), a("#gbox_" + a.jgrid.jqID(s.p.id))[0]), M && (a("#pData, #nData", A + "_2").css("float", "right"), a(".EditButton", A + "_2").css("text-align", "left")), b[s.p.id].topinfo && a(".tinfo", y).show(), b[s.p.id].bottominfo && a(".binfo", y).show(), W = null, T = null, a("#" + a.jgrid.jqID(B.themodal)).keydown(function (c) {
                            var
                            e = c.target;
                            if (!0 === a(y).data("disabled")) return !1;
                            if (!0 === b[s.p.id].savekey[0] && c.which === b[s.p.id].savekey[1] && "TEXTAREA" !== e.tagName) return a("#sData", A + "_2").trigger("click"), !1;
                            if (27 === c.which) return !!m() && (V && a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                gb: d.gbox,
                                jqm: d.jqModal,
                                onClose: b[s.p.id].onClose,
                                removemodal: b[s.p.id].removemodal,
                                formprop: !b[s.p.id].recreateForm,
                                form: b[s.p.id].form
                            }), !1);
                            if (!0 === b[s.p.id].navkeys[0]) {
                                if ("_empty" === a("#id_g", A).val()) return !0;
                                if (c.which === b[s.p.id].navkeys[1]) return a("#pData", t).trigger("click"), !1;
                                if (c.which === b[s.p.id].navkeys[2]) return a("#nData", t).trigger("click"), !1
                            }
                        }), d.checkOnUpdate && (a("a.ui-jqdialog-titlebar-close span", "#" + a.jgrid.jqID(B.themodal)).removeClass("jqmClose"), a("a.ui-jqdialog-titlebar-close", "#" + a.jgrid.jqID(B.themodal)).off("click").click(function () {
                            return !!m() && (a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(x),
                                jqm: d.jqModal,
                                onClose: b[s.p.id].onClose,
                                removemodal: b[s.p.id].removemodal,
                                formprop: !b[s.p.id].recreateForm,
                                form: b[s.p.id].form
                            }), !1)
                        })), d.saveicon = a.extend([!0, "left", g.icon_save], d.saveicon), d.closeicon = a.extend([!0, "left", g.icon_close], d.closeicon), !0 === d.saveicon[0] && a("#sData", t).addClass("right" === d.saveicon[1] ? "fm-button-icon-right" : "fm-button-icon-left").append("<span class='" + h.icon_base + " " + d.saveicon[2] + "'></span>"), !0 === d.closeicon[0] && a("#cData", t).addClass("right" === d.closeicon[1] ? "fm-button-icon-right" : "fm-button-icon-left").append("<span class='" + h.icon_base + " " + d.closeicon[2] + "'></span>"), b[s.p.id].checkOnSubmit || b[s.p.id].checkOnUpdate) {
                            R = "<a id='sNew' class='fm-button " + h.button + "' style='z-index:1002'>" + d.bYes + "</a>", Q = "<a id='nNew' class='fm-button " + h.button + "' style='z-index:1002;margin-left:5px'>" + d.bNo + "</a>", S = "<a id='cNew' class='fm-button " + h.button + "' style='z-index:1002;margin-left:5px;'>" + d.bExit + "</a>";
                            var
                            X = d.zIndex || 999;
                            X++, a("<div class='" + d.overlayClass + " jqgrid-overlay confirm' style='z-index:" + X + ";display:none;'>&#160;</div><div class='confirm ui-jqconfirm " + h.content + "' style='z-index:" + (X + 1) + "'>" + d.saveData + "<br/><br/>" + R + Q + S + "</div>").insertAfter(y), a("#sNew", "#" + a.jgrid.jqID(B.themodal)).click(function () {
                                return k(), a(y).data("disabled", !1), a(".confirm", "#" + a.jgrid.jqID(B.themodal)).hide(), !1
                            }), a("#nNew", "#" + a.jgrid.jqID(B.themodal)).click(function () {
                                return a(".confirm", "#" + a.jgrid.jqID(B.themodal)).hide(), a(y).data("disabled", !1), setTimeout(function () {
                                    a(":input:visible", y)[0].focus()
                                }, 0), !1
                            }), a("#cNew", "#" + a.jgrid.jqID(B.themodal)).click(function () {
                                return a(".confirm", "#" + a.jgrid.jqID(B.themodal)).hide(), a(y).data("disabled", !1), a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                    gb: "#gbox_" + a.jgrid.jqID(x),
                                    jqm: d.jqModal,
                                    onClose: b[s.p.id].onClose,
                                    removemodal: b[s.p.id].removemodal,
                                    formprop: !b[s.p.id].recreateForm,
                                    form: b[s.p.id].form
                                }), !1
                            })
                        }
                        a(s).triggerHandler("jqGridAddEditInitializeForm", [a(y), w]), a.isFunction(b[s.p.id].onInitializeForm) && b[s.p.id].onInitializeForm.call(s, a(y), w), "_empty" !== c && b[s.p.id].viewPagerButtons ? a("#pData,#nData", t).show() : a("#pData,#nData", t).hide(), a(s).triggerHandler("jqGridAddEditBeforeShowForm", [a(y), w]), a.isFunction(b[s.p.id].beforeShowForm) && b[s.p.id].beforeShowForm.call(s, a(y), w), r(), a("#" + a.jgrid.jqID(B.themodal)).data("onClose", b[s.p.id].onClose), a.jgrid.viewModal("#" + a.jgrid.jqID(B.themodal), {
                            gbox: "#gbox_" + a.jgrid.jqID(x),
                            jqm: d.jqModal,
                            overlay: d.overlay,
                            modal: d.modal,
                            overlayClass: d.overlayClass,
                            focusField: d.focusField,
                            onHide: function (b) {
                                var
                                c = a("#editmod" + x)[0].style.height,
                                    d = a("#editmod" + x)[0].style.width;
                                c.indexOf("px") > -1 && (c = parseFloat(c)), d.indexOf("px") > -1 && (d = parseFloat(d)), a(s).data("formProp", {
                                    top: parseFloat(a(b.w).css("top")),
                                    left: parseFloat(a(b.w).css("left")),
                                    width: d,
                                    height: c,
                                    dataheight: a(y).height(),
                                    datawidth: a(y).width()
                                }), b.w.remove(), b.o && b.o.remove()
                            }
                        }), H || a("." + a.jgrid.jqID(d.overlayClass)).click(function () {
                            return !!m() && (a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(x),
                                jqm: d.jqModal,
                                onClose: b[s.p.id].onClose,
                                removemodal: b[s.p.id].removemodal,
                                formprop: !b[s.p.id].recreateForm,
                                form: b[s.p.id].form
                            }), !1)
                        }), a(".fm-button", "#" + a.jgrid.jqID(B.themodal)).hover(function () {
                            a(this).addClass(h.hover)
                        }, function () {
                            a(this).removeClass(h.hover)
                        }), a("#sData", t).click(function () {
                            return u = {}, a(".FormError", y).hide(), e(), "_empty" === u[s.p.id + "_id"] ? k() : !0 === d.checkOnSubmit ? (v = l(u, s.p.savedData), v ? (a(y).data("disabled", !0), a(".confirm", "#" + a.jgrid.jqID(B.themodal)).show()) : k()) : k(), !1
                        }), a("#cData", t).click(function () {
                            return !!m() && (a.jgrid.hideModal("#" + a.jgrid.jqID(B.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(x),
                                jqm: d.jqModal,
                                onClose: b[s.p.id].onClose,
                                removemodal: b[s.p.id].removemodal,
                                formprop: !b[s.p.id].recreateForm,
                                form: b[s.p.id].form
                            }), !1)
                        }), a("#nData", t).click(function () {
                            if (!m()) return !1;
                            a(".FormError", y).hide();
                            var
                            c = p();
                            if (c[0] = parseInt(c[0], 10), -1 !== c[0] && c[1][c[0] + 1]) {
                                a(s).triggerHandler("jqGridAddEditClickPgButtons", ["next", a(y), c[1][c[0]]]);
                                var
                                e;
                                if (a.isFunction(d.onclickPgButtons) && void
                                0 !== (e = d.onclickPgButtons.call(s, "next", a(y), c[1][c[0]])) && !1 === e) return !1;
                                if (a("#" + a.jgrid.jqID(c[1][c[0] + 1])).hasClass(h.disabled)) return !1;
                                i(c[1][c[0] + 1], s, y), s.p.multiselect && b[s.p.id].editselected || a(s).jqGrid("setSelection", c[1][c[0] + 1]), a(s).triggerHandler("jqGridAddEditAfterClickPgButtons", ["next", a(y), c[1][c[0]]]), a.isFunction(d.afterclickPgButtons) && d.afterclickPgButtons.call(s, "next", a(y), c[1][c[0] + 1]), r(), o(c[0] + 1, c)
                            }
                            return !1
                        }), a("#pData", t).click(function () {
                            if (!m()) return !1;
                            a(".FormError", y).hide();
                            var
                            c = p();
                            if (-1 !== c[0] && c[1][c[0] - 1]) {
                                a(s).triggerHandler("jqGridAddEditClickPgButtons", ["prev", a(y), c[1][c[0]]]);
                                var
                                e;
                                if (a.isFunction(d.onclickPgButtons) && void
                                0 !== (e = d.onclickPgButtons.call(s, "prev", a(y), c[1][c[0]])) && !1 === e) return !1;
                                if (a("#" + a.jgrid.jqID(c[1][c[0] - 1])).hasClass(h.disabled)) return !1;
                                i(c[1][c[0] - 1], s, y), s.p.multiselect && b[s.p.id].editselected || a(s).jqGrid("setSelection", c[1][c[0] - 1]), a(s).triggerHandler("jqGridAddEditAfterClickPgButtons", ["prev", a(y), c[1][c[0]]]), a.isFunction(d.afterclickPgButtons) && d.afterclickPgButtons.call(s, "prev", a(y), c[1][c[0] - 1]), r(), o(c[0] - 1, c)
                            }
                            return !1
                        }), a(s).triggerHandler("jqGridAddEditAfterShowForm", [a(y), w]), a.isFunction(b[s.p.id].afterShowForm) && b[s.p.id].afterShowForm.call(s, a(y), w);
                        var
                        Y = p();
                        o(Y[0], Y)
                    }
                }
            })
        },
        viewGridRow: function (c, d) {
            var
            e = a.jgrid.getRegional(this[0], "view"),
                f = this[0].p.styleUI,
                g = a.jgrid.styleUI[f].formedit,
                h = a.jgrid.styleUI[f].common;
            return d = a.extend(!0, {
                top: 0,
                left: 0,
                width: 500,
                datawidth: "auto",
                height: "auto",
                dataheight: "auto",
                modal: !1,
                overlay: 30,
                drag: !0,
                resize: !0,
                jqModal: !0,
                closeOnEscape: !1,
                labelswidth: "30%",
                closeicon: [],
                navkeys: [!1, 38, 40],
                onClose: null,
                beforeShowForm: null,
                beforeInitData: null,
                viewPagerButtons: !0,
                recreateForm: !1,
                removemodal: !0,
                form: "view"
            }, e, d || {}), b[a(this)[0].p.id] = d, this.each(function () {
                function
                e() {
                    !0 !== b[l.p.id].closeOnEscape && !0 !== b[l.p.id].navkeys[0] || setTimeout(function () {
                        a(".ui-jqdialog-titlebar-close", "#" + a.jgrid.jqID(r.modalhead)).attr("tabindex", "-1").focus()
                    }, 0)
                }

                function
                f(b, c, e, f) {
                    var
                    g, i, j, k, l, m, n, o, p, q = 0,
                        r = [],
                        s = !1,
                        t = "<td class='CaptionTD form-view-label " + h.content + "' width='" + d.labelswidth + "'>&#160;</td><td class='DataTD form-view-data ui-helper-reset " + h.content + "'>&#160;</td>",
                        u = "",
                        v = "<td class='CaptionTD form-view-label " + h.content + "'>&#160;</td><td class='DataTD form-view-data " + h.content + "'>&#160;</td>",
                        w = ["integer", "number", "currency"],
                        x = 0,
                        y = 0;
                    for (m = 1; m <= f; m++) u += 1 === m ? t : v;
                    if (a(c.p.colModel).each(function () {
                        (i = (!this.editrules || !0 !== this.editrules.edithidden) && !0 === this.hidden) || "right" !== this.align || (this.formatter && -1 !== a.inArray(this.formatter, w) ? x = Math.max(x, parseInt(this.width, 10)) : y = Math.max(y, parseInt(this.width, 10)))
                    }), n = 0 !== x ? x : 0 !== y ? y : 0, s = a(c).jqGrid("getInd", b), a(c.p.colModel).each(function (b) {
                        if (g = this.name, o = !1, i = (!this.editrules || !0 !== this.editrules.edithidden) && !0 === this.hidden, l = i ? "style='display:none'" : "", p = "boolean" != typeof
                        this.viewable || this.viewable, "cb" !== g && "subgrid" !== g && "rn" !== g && p) {
                            k = !1 === s ? "" : g === c.p.ExpandColumn && !0 === c.p.treeGrid ? a("td:eq(" + b + ")", c.rows[s]).text() : a("td:eq(" + b + ")", c.rows[s]).html(), o = "right" === this.align && 0 !== n;
                            var
                            d = a.extend({}, {
                                rowabove: !1,
                                rowcontent: ""
                            }, this.formoptions || {}),
                                h = parseInt(d.rowpos, 10) || q + 1,
                                m = parseInt(2 * (parseInt(d.colpos, 10) || 1), 10);
                            if (d.rowabove) {
                                var
                                t = a("<tr><td class='contentinfo' colspan='" + 2 * f + "'>" + d.rowcontent + "</td></tr>");
                                a(e).append(t), t[0].rp = h
                            }
                            j = a(e).find("tr[rowpos=" + h + "]"), 0 === j.length && (j = a("<tr " + l + " rowpos='" + h + "'></tr>").addClass("FormData").attr("id", "trv_" + g), a(j).append(u), a(e).append(j), j[0].rp = h), a("td:eq(" + (m - 2) + ")", j[0]).html("<b>" + (void
                            0 === d.label ? c.p.colNames[b] : d.label) + "</b>"), a("td:eq(" + (m - 1) + ")", j[0]).append("<span>" + k + "</span>").attr("id", "v_" + g), o && a("td:eq(" + (m - 1) + ") span", j[0]).css({
                                "text-align": "right",
                                width: n + "px"
                            }), r[q] = b, q++
                        }
                    }), q > 0) {
                        var
                        z = a("<tr class='FormData' style='display:none'><td class='CaptionTD'></td><td colspan='" + (2 * f - 1) + "' class='DataTD'><input class='FormElement' id='id_g' type='text' name='id' value='" + b + "'/></td></tr>");
                        z[0].rp = q + 99, a(e).append(z)
                    }
                    return r
                }

                function
                i(b, c) {
                    var
                    d, e, f, g, h = 0;
                    (g = a(c).jqGrid("getInd", b, !0)) && (a("td", g).each(function (b) {
                        d = c.p.colModel[b].name, e = (!c.p.colModel[b].editrules || !0 !== c.p.colModel[b].editrules.edithidden) && !0 === c.p.colModel[b].hidden, "cb" !== d && "subgrid" !== d && "rn" !== d && (f = d === c.p.ExpandColumn && !0 === c.p.treeGrid ? a(this).text() : a(this).html(), d = a.jgrid.jqID("v_" + d), a("#" + d + " span", "#" + o).html(f), e && a("#" + d, "#" + o).parents("tr:first").hide(), h++)
                    }), h > 0 && a("#id_g", "#" + o).val(b))
                }

                function
                j(b, c) {
                    var
                    d = c[1].length - 1;
                    0 === b ? a("#pData", "#" + o + "_2").addClass(h.disabled) : void
                    0 !== c[1][b - 1] && a("#" + a.jgrid.jqID(c[1][b - 1])).hasClass(h.disabled) ? a("#pData", o + "_2").addClass(h.disabled) : a("#pData", "#" + o + "_2").removeClass(h.disabled), b === d ? a("#nData", "#" + o + "_2").addClass(h.disabled) : void
                    0 !== c[1][b + 1] && a("#" + a.jgrid.jqID(c[1][b + 1])).hasClass(h.disabled) ? a("#nData", o + "_2").addClass(h.disabled) : a("#nData", "#" + o + "_2").removeClass(h.disabled)
                }

                function
                k() {
                    var
                    b = a(l).jqGrid("getDataIDs"),
                        c = a("#id_g", "#" + o).val();
                    return [a.inArray(c, b), b]
                }
                var
                l = this;
                if (l.grid && c) {
                    var
                    m = l.p.id,
                        n = "ViewGrid_" + a.jgrid.jqID(m),
                        o = "ViewTbl_" + a.jgrid.jqID(m),
                        p = "ViewGrid_" + m,
                        q = "ViewTbl_" + m,
                        r = {
                            themodal: "viewmod" + m,
                            modalhead: "viewhd" + m,
                            modalcontent: "viewcnt" + m,
                            scrollelm: n
                        }, s = !0,
                        t = 1,
                        u = 0;
                    b[l.p.id].styleUI = l.p.styleUI || "jQueryUI", d.recreateForm || a(l).data("viewProp") && a.extend(b[a(this)[0].p.id], a(l).data("viewProp"));
                    var
                    v = isNaN(b[a(this)[0].p.id].dataheight) ? b[a(this)[0].p.id].dataheight : b[a(this)[0].p.id].dataheight + "px",
                        w = isNaN(b[a(this)[0].p.id].datawidth) ? b[a(this)[0].p.id].datawidth : b[a(this)[0].p.id].datawidth + "px",
                        x = a("<form name='FormPost' id='" + p + "' class='FormGrid' style='width:" + w + ";height:" + v + ";'></form>"),
                        y = a("<table id='" + q + "' class='EditTable ViewTable'><tbody></tbody></table>");
                    if (a(l.p.colModel).each(function () {
                        var
                        a = this.formoptions;
                        t = Math.max(t, a ? a.colpos || 0 : 0), u = Math.max(u, a ? a.rowpos || 0 : 0)
                    }), a(x).append(y), s = a(l).triggerHandler("jqGridViewRowBeforeInitData", [x]), void
                    0 === s && (s = !0), s && a.isFunction(b[l.p.id].beforeInitData) && (s = b[l.p.id].beforeInitData.call(l, x)), !1 !== s) {
                        f(c, l, y, t);
                        var
                        z = "rtl" === l.p.direction,
                            A = z ? "nData" : "pData",
                            B = z ? "pData" : "nData",
                            C = "<a id='" + A + "' class='fm-button " + h.button + "'><span class='" + h.icon_base + " " + g.icon_prev + "'></span></a>",
                            D = "<a id='" + B + "' class='fm-button " + h.button + "'><span class='" + h.icon_base + " " + g.icon_next + "'></span></a>",
                            E = "<a id='cData' class='fm-button " + h.button + "'>" + d.bClose + "</a>";
                        if (u > 0) {
                            var
                            F = [];
                            a.each(a(y)[0].rows, function (a, b) {
                                F[a] = b
                            }), F.sort(function (a, b) {
                                return a.rp > b.rp ? 1 : a.rp < b.rp ? -1 : 0
                            }), a.each(F, function (b, c) {
                                a("tbody", y).append(c)
                            })
                        }
                        d.gbox = "#gbox_" + a.jgrid.jqID(m);
                        var
                        G = a("<div></div>").append(x).append("<table border='0' class='EditTable' id='" + o + "_2'><tbody><tr id='Act_Buttons'><td class='navButton' width='" + d.labelswidth + "'>" + (z ? D + C : C + D) + "</td><td class='EditButton'>" + E + "</td></tr></tbody></table>");
                        a.jgrid.createModal(r, G, b[a(this)[0].p.id], "#gview_" + a.jgrid.jqID(l.p.id), a("#gview_" + a.jgrid.jqID(l.p.id))[0]), z && (a("#pData, #nData", "#" + o + "_2").css("float", "right"), a(".EditButton", "#" + o + "_2").css("text-align", "left")), d.viewPagerButtons || a("#pData, #nData", "#" + o + "_2").hide(), G = null, a("#" + r.themodal).keydown(function (c) {
                            if (27 === c.which) return b[l.p.id].closeOnEscape && a.jgrid.hideModal("#" + a.jgrid.jqID(r.themodal), {
                                gb: d.gbox,
                                jqm: d.jqModal,
                                onClose: d.onClose,
                                removemodal: b[l.p.id].removemodal,
                                formprop: !b[l.p.id].recreateForm,
                                form: b[l.p.id].form
                            }), !1;
                            if (!0 === d.navkeys[0]) {
                                if (c.which === d.navkeys[1]) return a("#pData", "#" + o + "_2").trigger("click"), !1;
                                if (c.which === d.navkeys[2]) return a("#nData", "#" + o + "_2").trigger("click"), !1
                            }
                        }), d.closeicon = a.extend([!0, "left", g.icon_close], d.closeicon), !0 === d.closeicon[0] && a("#cData", "#" + o + "_2").addClass("right" === d.closeicon[1] ? "fm-button-icon-right" : "fm-button-icon-left").append("<span class='" + h.icon_base + " " + d.closeicon[2] + "'></span>"), a(l).triggerHandler("jqGridViewRowBeforeShowForm", [a("#" + n)]), a.isFunction(d.beforeShowForm) && d.beforeShowForm.call(l, a("#" + n)), a.jgrid.viewModal("#" + a.jgrid.jqID(r.themodal), {
                            gbox: "#gbox_" + a.jgrid.jqID(m),
                            jqm: d.jqModal,
                            overlay: d.overlay,
                            modal: d.modal,
                            onHide: function (b) {
                                a(l).data("viewProp", {
                                    top: parseFloat(a(b.w).css("top")),
                                    left: parseFloat(a(b.w).css("left")),
                                    width: a(b.w).width(),
                                    height: a(b.w).height(),
                                    dataheight: a("#" + n).height(),
                                    datawidth: a("#" + n).width()
                                }), b.w.remove(), b.o && b.o.remove()
                            }
                        }), a(".fm-button:not(." + h.disabled + ")", "#" + o + "_2").hover(function () {
                            a(this).addClass(h.hover)
                        }, function () {
                            a(this).removeClass(h.hover)
                        }), e(), a("#cData", "#" + o + "_2").click(function () {
                            return a.jgrid.hideModal("#" + a.jgrid.jqID(r.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(m),
                                jqm: d.jqModal,
                                onClose: d.onClose,
                                removemodal: b[l.p.id].removemodal,
                                formprop: !b[l.p.id].recreateForm,
                                form: b[l.p.id].form
                            }), !1
                        }), a("#nData", "#" + o + "_2").click(function () {
                            a("#FormError", "#" + o).hide();
                            var
                            b = k();
                            return b[0] = parseInt(b[0], 10), -1 !== b[0] && b[1][b[0] + 1] && (a(l).triggerHandler("jqGridViewRowClickPgButtons", ["next", a("#" + n), b[1][b[0]]]), a.isFunction(d.onclickPgButtons) && d.onclickPgButtons.call(l, "next", a("#" + n), b[1][b[0]]), i(b[1][b[0] + 1], l), a(l).jqGrid("setSelection", b[1][b[0] + 1]), a(l).triggerHandler("jqGridViewRowAfterClickPgButtons", ["next", a("#" + n), b[1][b[0] + 1]]), a.isFunction(d.afterclickPgButtons) && d.afterclickPgButtons.call(l, "next", a("#" + n), b[1][b[0] + 1]), j(b[0] + 1, b)), e(), !1
                        }), a("#pData", "#" + o + "_2").click(function () {
                            a("#FormError", "#" + o).hide();
                            var
                            b = k();
                            return -1 !== b[0] && b[1][b[0] - 1] && (a(l).triggerHandler("jqGridViewRowClickPgButtons", ["prev", a("#" + n), npos[1][npos[0]]]), a.isFunction(d.onclickPgButtons) && d.onclickPgButtons.call(l, "prev", a("#" + n), b[1][b[0]]), i(b[1][b[0] - 1], l), a(l).jqGrid("setSelection", b[1][b[0] - 1]), a(l).triggerHandler("jqGridViewRowAfterClickPgButtons", ["prev", a("#" + n), npos[1][npos[0] - 1]]), a.isFunction(d.afterclickPgButtons) && d.afterclickPgButtons.call(l, "prev", a("#" + n), b[1][b[0] - 1]), j(b[0] - 1, b)), e(), !1
                        });
                        var
                        H = k();
                        j(H[0], H)
                    }
                }
            })
        },
        delGridRow: function (c, d) {
            var
            e = a.jgrid.getRegional(this[0], "del"),
                f = this[0].p.styleUI,
                g = a.jgrid.styleUI[f].formedit,
                h = a.jgrid.styleUI[f].common;
            return d = a.extend(!0, {
                top: 0,
                left: 0,
                width: 240,
                height: "auto",
                dataheight: "auto",
                modal: !1,
                overlay: 30,
                drag: !0,
                resize: !0,
                url: "",
                mtype: "POST",
                reloadAfterSubmit: !0,
                beforeShowForm: null,
                beforeInitData: null,
                afterShowForm: null,
                beforeSubmit: null,
                onclickSubmit: null,
                afterSubmit: null,
                jqModal: !0,
                closeOnEscape: !1,
                delData: {},
                delicon: [],
                cancelicon: [],
                onClose: null,
                ajaxDelOptions: {},
                processing: !1,
                serializeDelData: null,
                useDataProxy: !1
            }, e, d || {}), b[a(this)[0].p.id] = d, this.each(function () {
                var
                e = this;
                if (e.grid && c) {
                    var
                    f, i, j, k, l = e.p.id,
                        m = {}, n = !0,
                        o = "DelTbl_" + a.jgrid.jqID(l),
                        p = "DelTbl_" + l,
                        q = {
                            themodal: "delmod" + l,
                            modalhead: "delhd" + l,
                            modalcontent: "delcnt" + l,
                            scrollelm: o
                        };
                    if (b[e.p.id].styleUI = e.p.styleUI || "jQueryUI", a.isArray(c) && (c = c.join()), void
                    0 !== a("#" + a.jgrid.jqID(q.themodal))[0]) {
                        if (n = a(e).triggerHandler("jqGridDelRowBeforeInitData", [a("#" + o)]), void
                        0 === n && (n = !0), n && a.isFunction(b[e.p.id].beforeInitData) && (n = b[e.p.id].beforeInitData.call(e, a("#" + o))), !1 === n) return;
                        a("#DelData>td", "#" + o).text(c), a("#DelError", "#" + o).hide(), !0 === b[e.p.id].processing && (b[e.p.id].processing = !1, a("#dData", "#" + o).removeClass(h.active)), a(e).triggerHandler("jqGridDelRowBeforeShowForm", [a("#" + o)]), a.isFunction(b[e.p.id].beforeShowForm) && b[e.p.id].beforeShowForm.call(e, a("#" + o)), a.jgrid.viewModal("#" + a.jgrid.jqID(q.themodal), {
                            gbox: "#gbox_" + a.jgrid.jqID(l),
                            jqm: b[e.p.id].jqModal,
                            overlay: b[e.p.id].overlay,
                            modal: b[e.p.id].modal
                        }), a(e).triggerHandler("jqGridDelRowAfterShowForm", [a("#" + o)]), a.isFunction(b[e.p.id].afterShowForm) && b[e.p.id].afterShowForm.call(e, a("#" + o))
                    } else {
                        var
                        r = isNaN(b[e.p.id].dataheight) ? b[e.p.id].dataheight : b[e.p.id].dataheight + "px",
                            s = isNaN(d.datawidth) ? d.datawidth : d.datawidth + "px",
                            t = "<div id='" + p + "' class='formdata' style='width:" + s + ";overflow:auto;position:relative;height:" + r + ";'>";
                        t += "<table class='DelTable'><tbody>", t += "<tr id='DelError' style='display:none'><td class='" + h.error + "'></td></tr>", t += "<tr id='DelData' style='display:none'><td >" + c + "</td></tr>", t += '<tr><td class="delmsg" style="white-space:pre;">' + b[e.p.id].msg + "</td></tr><tr><td >&#160;</td></tr>", t += "</tbody></table></div>";
                        var
                        u = "<a id='dData' class='fm-button " + h.button + "'>" + d.bSubmit + "</a>",
                            v = "<a id='eData' class='fm-button " + h.button + "'>" + d.bCancel + "</a>";
                        if (t += "<table class='EditTable ui-common-table' id='" + o + "_2'><tbody><tr><td><hr class='" + h.content + "' style='margin:1px'/></td></tr><tr><td class='DelButton EditButton'>" + u + "&#160;" + v + "</td></tr></tbody></table>", d.gbox = "#gbox_" + a.jgrid.jqID(l), a.jgrid.createModal(q, t, b[e.p.id], "#gview_" + a.jgrid.jqID(e.p.id), a("#gview_" + a.jgrid.jqID(e.p.id))[0]), a(".fm-button", "#" + o + "_2").hover(function () {
                            a(this).addClass(h.hover)
                        }, function () {
                            a(this).removeClass(h.hover)
                        }), d.delicon = a.extend([!0, "left", g.icon_del], b[e.p.id].delicon), d.cancelicon = a.extend([!0, "left", g.icon_cancel], b[e.p.id].cancelicon), !0 === d.delicon[0] && a("#dData", "#" + o + "_2").addClass("right" === d.delicon[1] ? "fm-button-icon-right" : "fm-button-icon-left").append("<span class='" + h.icon_base + " " + d.delicon[2] + "'></span>"), !0 === d.cancelicon[0] && a("#eData", "#" + o + "_2").addClass("right" === d.cancelicon[1] ? "fm-button-icon-right" : "fm-button-icon-left").append("<span class='" + h.icon_base + " " + d.cancelicon[2] + "'></span>"), a("#dData", "#" + o + "_2").click(function () {
                            var
                            c, g = [!0, ""],
                                n = a("#DelData>td", "#" + o).text();
                            if (m = {}, m = a(e).triggerHandler("jqGridDelRowClickSubmit", [b[e.p.id], n]), void
                            0 === m && a.isFunction(b[e.p.id].onclickSubmit) && (m = b[e.p.id].onclickSubmit.call(e, b[e.p.id], n) || {}), g = a(e).triggerHandler("jqGridDelRowBeforeSubmit", [n]), void
                            0 === g && (g = [!0, "", ""]), g[0] && a.isFunction(b[e.p.id].beforeSubmit) && (g = b[e.p.id].beforeSubmit.call(e, n)), g[0] && !b[e.p.id].processing) {
                                if (b[e.p.id].processing = !0, j = e.p.prmNames, f = a.extend({}, b[e.p.id].delData, m), k = j.oper, f[k] = j.deloper, i = j.id, n = String(n).split(","), !n.length) return !1;
                                for (c in n) n.hasOwnProperty(c) && (n[c] = a.jgrid.stripPref(e.p.idPrefix, n[c]));
                                f[i] = n.join(), a(this).addClass(h.active);
                                var
                                p = a.extend({
                                    url: b[e.p.id].url || a(e).jqGrid("getGridParam", "editurl"),
                                    type: b[e.p.id].mtype,
                                    data: a.isFunction(b[e.p.id].serializeDelData) ? b[e.p.id].serializeDelData.call(e, f) : f,
                                    complete: function (c, i) {
                                        var
                                        j;
                                        if (a("#dData", "#" + o + "_2").removeClass(h.active), c.status >= 300 && 304 !== c.status ? (g[0] = !1, g[1] = a(e).triggerHandler("jqGridDelRowErrorTextFormat", [c]), a.isFunction(b[e.p.id].errorTextFormat) && (g[1] = b[e.p.id].errorTextFormat.call(e, c)), void
                                        0 === g[1] && (g[1] = i + " Status: '" + c.statusText + "'. Error code: " + c.status)) : (g = a(e).triggerHandler("jqGridDelRowAfterSubmit", [c, f]), void
                                        0 === g && (g = [!0, "", ""]), g[0] && a.isFunction(b[e.p.id].afterSubmit) && (g = b[e.p.id].afterSubmit.call(e, c, f))), !1 === g[0]) a("#DelError>td", "#" + o).html(g[1]), a("#DelError", "#" + o).show();
                                        else {
                                            if (b[e.p.id].reloadAfterSubmit && "local" !== e.p.datatype) a(e).trigger("reloadGrid");
                                            else {
                                                if (!0 === e.p.treeGrid) try {
                                                    a(e).jqGrid("delTreeNode", e.p.idPrefix + n[0])
                                                } catch (a) {} else for (j = 0; j < n.length; j++) a(e).jqGrid("delRowData", e.p.idPrefix + n[j]);
                                                e.p.selrow = null, e.p.selarrrow = []
                                            }
                                            if (a.isFunction(b[e.p.id].afterComplete) || a._data(a(e)[0], "events").hasOwnProperty("jqGridDelRowAfterComplete")) {
                                                var
                                                k = c;
                                                setTimeout(function () {
                                                    a(e).triggerHandler("jqGridDelRowAfterComplete", [k, f]);
                                                    try {
                                                        b[e.p.id].afterComplete.call(e, k, f)
                                                    } catch (a) {}
                                                }, 500)
                                            }
                                        }
                                        b[e.p.id].processing = !1, g[0] && a.jgrid.hideModal("#" + a.jgrid.jqID(q.themodal), {
                                            gb: "#gbox_" + a.jgrid.jqID(l),
                                            jqm: d.jqModal,
                                            onClose: b[e.p.id].onClose
                                        })
                                    }
                                }, a.jgrid.ajaxOptions, b[e.p.id].ajaxDelOptions);
                                if (p.url || b[e.p.id].useDataProxy || (a.isFunction(e.p.dataProxy) ? b[e.p.id].useDataProxy = !0 : (g[0] = !1, g[1] += " " + a.jgrid.getRegional(e, "errors.nourl"))), g[0]) if (b[e.p.id].useDataProxy) {
                                    var
                                    r = e.p.dataProxy.call(e, p, "del_" + e.p.id);
                                    void
                                    0 === r && (r = [!0, ""]), !1 === r[0] ? (g[0] = !1, g[1] = r[1] || "Error deleting the selected row!") : a.jgrid.hideModal("#" + a.jgrid.jqID(q.themodal), {
                                        gb: "#gbox_" + a.jgrid.jqID(l),
                                        jqm: d.jqModal,
                                        onClose: b[e.p.id].onClose
                                    })
                                } else "clientArray" === p.url ? (f = p.data, p.complete({
                                    status: 200,
                                    statusText: ""
                                }, "")) : a.ajax(p)
                            }
                            return !1 === g[0] && (a("#DelError>td", "#" + o).html(g[1]), a("#DelError", "#" + o).show()), !1
                        }), a("#eData", "#" + o + "_2").click(function () {
                            return a.jgrid.hideModal("#" + a.jgrid.jqID(q.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(l),
                                jqm: b[e.p.id].jqModal,
                                onClose: b[e.p.id].onClose
                            }), !1
                        }), n = a(e).triggerHandler("jqGridDelRowBeforeInitData", [a("#" + o)]), void
                        0 === n && (n = !0), n && a.isFunction(b[e.p.id].beforeInitData) && (n = b[e.p.id].beforeInitData.call(e, a("#" + o))), !1 === n) return;
                        a(e).triggerHandler("jqGridDelRowBeforeShowForm", [a("#" + o)]), a.isFunction(b[e.p.id].beforeShowForm) && b[e.p.id].beforeShowForm.call(e, a("#" + o)), a.jgrid.viewModal("#" + a.jgrid.jqID(q.themodal), {
                            gbox: "#gbox_" + a.jgrid.jqID(l),
                            jqm: b[e.p.id].jqModal,
                            overlay: b[e.p.id].overlay,
                            modal: b[e.p.id].modal
                        }), a(e).triggerHandler("jqGridDelRowAfterShowForm", [a("#" + o)]), a.isFunction(b[e.p.id].afterShowForm) && b[e.p.id].afterShowForm.call(e, a("#" + o))
                    }!0 === b[e.p.id].closeOnEscape && setTimeout(function () {
                        a(".ui-jqdialog-titlebar-close", "#" + a.jgrid.jqID(q.modalhead)).attr("tabindex", "-1").focus()
                    }, 0)
                }
            })
        },
        navGrid: function (b, c, d, e, f, g, h) {
            var
            i = a.jgrid.getRegional(this[0], "nav"),
                j = this[0].p.styleUI,
                k = a.jgrid.styleUI[j].navigator,
                l = a.jgrid.styleUI[j].common;
            return c = a.extend({
                edit: !0,
                editicon: k.icon_edit_nav,
                add: !0,
                addicon: k.icon_add_nav,
                del: !0,
                delicon: k.icon_del_nav,
                search: !0,
                searchicon: k.icon_search_nav,
                refresh: !0,
                refreshicon: k.icon_refresh_nav,
                refreshstate: "firstpage",
                view: !1,
                viewicon: k.icon_view_nav,
                position: "left",
                closeOnEscape: !0,
                beforeRefresh: null,
                afterRefresh: null,
                cloneToTop: !1,
                alertwidth: 200,
                alertheight: "auto",
                alerttop: null,
                alertleft: null,
                alertzIndex: null,
                dropmenu: !1,
                navButtonText: ""
            }, i, c || {}), this.each(function () {
                if (!this.p.navGrid) {
                    var
                    k, m, n, o = {
                        themodal: "alertmod_" + this.p.id,
                        modalhead: "alerthd_" + this.p.id,
                        modalcontent: "alertcnt_" + this.p.id
                    }, p = this;
                    if (p.grid && "string" == typeof
                    b) {
                        a(p).data("navGrid") || a(p).data("navGrid", c), n = a(p).data("navGrid"), p.p.force_regional && (n = a.extend(n, i)), void
                        0 === a("#" + o.themodal)[0] && (n.alerttop || n.alertleft || (void
                        0 !== window.innerWidth ? (n.alertleft = window.innerWidth, n.alerttop = window.innerHeight) : void
                        0 !== document.documentElement && void
                        0 !== document.documentElement.clientWidth && 0 !== document.documentElement.clientWidth ? (n.alertleft = document.documentElement.clientWidth, n.alerttop = document.documentElement.clientHeight) : (n.alertleft = 1024, n.alerttop = 768), n.alertleft = n.alertleft / 2 - parseInt(n.alertwidth, 10) / 2, n.alerttop = n.alerttop / 2 - 25), a.jgrid.createModal(o, "<div>" + n.alerttext + "</div><span tabindex='0'><span tabindex='-1' id='jqg_alrt'></span></span>", {
                            gbox: "#gbox_" + a.jgrid.jqID(p.p.id),
                            jqModal: !0,
                            drag: !0,
                            resize: !0,
                            caption: n.alertcap,
                            top: n.alerttop,
                            left: n.alertleft,
                            width: n.alertwidth,
                            height: n.alertheight,
                            closeOnEscape: n.closeOnEscape,
                            zIndex: n.alertzIndex,
                            styleUI: p.p.styleUI
                        }, "#gview_" + a.jgrid.jqID(p.p.id), a("#gbox_" + a.jgrid.jqID(p.p.id))[0], !0));
                        var
                        q, r = 1,
                            s = function () {
                                a(this).hasClass(l.disabled) || a(this).addClass(l.hover)
                            }, t = function () {
                                a(this).removeClass(l.hover)
                            };
                        for (n.cloneToTop && p.p.toppager && (r = 2), q = 0; q < r; q++) {
                            var
                            u, v, w, x = a("<table class='ui-pg-table navtable ui-common-table'><tbody><tr></tr></tbody></table>"),
                                y = "<td class='ui-pg-button " + l.disabled + "' style='width:4px;'><span class='ui-separator'></span></td>";
                            0 === q ? (v = b, w = p.p.id, v === p.p.toppager && (w += "_top", r = 1)) : (v = p.p.toppager, w = p.p.id + "_top"), "rtl" === p.p.direction && a(x).attr("dir", "rtl").css("float", "right"), e = e || {}, n.add && (u = a("<td class='ui-pg-button " + l.cornerall + "'></td>"), a(u).append("<div class='ui-pg-div'><span class='" + l.icon_base + " " + n.addicon + "'></span>" + n.addtext + "</div>"), a("tr", x).append(u), a(u, x).attr({
                                title: n.addtitle || "",
                                id: e.id || "add_" + w
                            }).click(function () {
                                return a(this).hasClass(l.disabled) || (a.isFunction(n.addfunc) ? n.addfunc.call(p) : a(p).jqGrid("editGridRow", "new", e)), !1
                            }).hover(s, t), u = null), d = d || {}, n.edit && (u = a("<td class='ui-pg-button " + l.cornerall + "'></td>"), a(u).append("<div class='ui-pg-div'><span class='" + l.icon_base + " " + n.editicon + "'></span>" + n.edittext + "</div>"), a("tr", x).append(u), a(u, x).attr({
                                title: n.edittitle || "",
                                id: d.id || "edit_" + w
                            }).click(function () {
                                if (!a(this).hasClass(l.disabled)) {
                                    var
                                    b = p.p.selrow;
                                    b ? a.isFunction(n.editfunc) ? n.editfunc.call(p, b) : a(p).jqGrid("editGridRow", b, d) : (a.jgrid.viewModal("#" + o.themodal, {
                                        gbox: "#gbox_" + a.jgrid.jqID(p.p.id),
                                        jqm: !0
                                    }), a("#jqg_alrt").focus())
                                }
                                return !1
                            }).hover(s, t), u = null), h = h || {}, n.view && (u = a("<td class='ui-pg-button " + l.cornerall + "'></td>"), a(u).append("<div class='ui-pg-div'><span class='" + l.icon_base + " " + n.viewicon + "'></span>" + n.viewtext + "</div>"), a("tr", x).append(u), a(u, x).attr({
                                title: n.viewtitle || "",
                                id: h.id || "view_" + w
                            }).click(function () {
                                if (!a(this).hasClass(l.disabled)) {
                                    var
                                    b = p.p.selrow;
                                    b ? a.isFunction(n.viewfunc) ? n.viewfunc.call(p, b) : a(p).jqGrid("viewGridRow", b, h) : (a.jgrid.viewModal("#" + o.themodal, {
                                        gbox: "#gbox_" + a.jgrid.jqID(p.p.id),
                                        jqm: !0
                                    }), a("#jqg_alrt").focus())
                                }
                                return !1
                            }).hover(s, t), u = null), f = f || {}, n.del && (u = a("<td class='ui-pg-button " + l.cornerall + "'></td>"), a(u).append("<div class='ui-pg-div'><span class='" + l.icon_base + " " + n.delicon + "'></span>" + n.deltext + "</div>"), a("tr", x).append(u), a(u, x).attr({
                                title: n.deltitle || "",
                                id: f.id || "del_" + w
                            }).click(function () {
                                if (!a(this).hasClass(l.disabled)) {
                                    var
                                    b;
                                    p.p.multiselect ? (b = p.p.selarrrow, 0 === b.length && (b = null)) : b = p.p.selrow, b ? a.isFunction(n.delfunc) ? n.delfunc.call(p, b) : a(p).jqGrid("delGridRow", b, f) : (a.jgrid.viewModal("#" + o.themodal, {
                                        gbox: "#gbox_" + a.jgrid.jqID(p.p.id),
                                        jqm: !0
                                    }), a("#jqg_alrt").focus())
                                }
                                return !1
                            }).hover(s, t), u = null), (n.add || n.edit || n.del || n.view) && a("tr", x).append(y), g = g || {}, n.search && (u = a("<td class='ui-pg-button " + l.cornerall + "'></td>"), a(u).append("<div class='ui-pg-div'><span class='" + l.icon_base + " " + n.searchicon + "'></span>" + n.searchtext + "</div>"), a("tr", x).append(u), a(u, x).attr({
                                title: n.searchtitle || "",
                                id: g.id || "search_" + w
                            }).click(function () {
                                return a(this).hasClass(l.disabled) || (a.isFunction(n.searchfunc) ? n.searchfunc.call(p, g) : a(p).jqGrid("searchGrid", g)), !1
                            }).hover(s, t), g.showOnLoad && !0 === g.showOnLoad && a(u, x).click(), u = null), n.refresh && (u = a("<td class='ui-pg-button " + l.cornerall + "'></td>"), a(u).append("<div class='ui-pg-div'><span class='" + l.icon_base + " " + n.refreshicon + "'></span>" + n.refreshtext + "</div>"), a("tr", x).append(u), a(u, x).attr({
                                title: n.refreshtitle || "",
                                id: "refresh_" + w
                            }).click(function () {
                                if (!a(this).hasClass(l.disabled)) {
                                    a.isFunction(n.beforeRefresh) && n.beforeRefresh.call(p), p.p.search = !1, p.p.resetsearch = !0;
                                    try {
                                        if ("currentfilter" !== n.refreshstate) {
                                            var
                                            b = p.p.id;
                                            p.p.postData.filters = "";
                                            try {
                                                a("#fbox_" + a.jgrid.jqID(b)).jqFilter("resetFilter")
                                            } catch (a) {}
                                            a.isFunction(p.clearToolbar) && p.clearToolbar.call(p, !1)
                                        }
                                    } catch (a) {}
                                    switch (n.refreshstate) {
                                        case "firstpage":
                                            a(p).trigger("reloadGrid", [{
                                                page: 1
                                            }]);
                                            break;
                                        case "current":
                                        case "currentfilter":
                                            a(p).trigger("reloadGrid", [{
                                                current: !0
                                            }])
                                    }
                                    a.isFunction(n.afterRefresh) && n.afterRefresh.call(p)
                                }
                                return !1
                            }).hover(s, t), u = null), m = a(".ui-jqgrid").css("font-size") || "11px", a("body").append("<div id='testpg2' class='ui-jqgrid " + a.jgrid.styleUI[j].base.entrieBox + "' style='font-size:" + m + ";visibility:hidden;' ></div>"), k = a(x).clone().appendTo("#testpg2").width(), a("#testpg2").remove(), p.p._nvtd && (n.dropmenu ? (x = null, a(p).jqGrid("_buildNavMenu", v, w, c, d, e, f, g, h)) : k > p.p._nvtd[0] ? (p.p.responsive ? (x = null, a(p).jqGrid("_buildNavMenu", v, w, c, d, e, f, g, h)) : a(v + "_" + n.position, v).append(x).width(k), p.p._nvtd[0] = k) : a(v + "_" + n.position, v).append(x), p.p._nvtd[1] = k), p.p.navGrid = !0
                        }
                        p.p.storeNavOptions && (p.p.navOptions = n, p.p.editOptions = d, p.p.addOptions = e, p.p.delOptions = f, p.p.searchOptions = g, p.p.viewOptions = h, p.p.navButtons = [])
                    }
                }
            })
        },
        navButtonAdd: function (b, c) {
            var
            d = this[0].p.styleUI,
                e = a.jgrid.styleUI[d].navigator;
            return c = a.extend({
                caption: "newButton",
                title: "",
                buttonicon: e.icon_newbutton_nav,
                onClickButton: null,
                position: "last",
                cursor: "pointer",
                internal: !1
            }, c || {}), this.each(function () {
                if (this.grid) {
                    "string" == typeof
                    b && 0 !== b.indexOf("#") && (b = "#" + a.jgrid.jqID(b));
                    var
                    e = a(".navtable", b)[0],
                        f = this,
                        g = a.jgrid.styleUI[d].common.disabled,
                        h = a.jgrid.styleUI[d].common.hover,
                        i = a.jgrid.styleUI[d].common.cornerall,
                        j = a.jgrid.styleUI[d].common.icon_base;
                    if (f.p.storeNavOptions && !c.internal && f.p.navButtons.push([b, c]), e) {
                        if (c.id && void
                        0 !== a("#" + a.jgrid.jqID(c.id), e)[0]) return;
                        var
                        k = a("<td></td>");
                        "NONE" === c.buttonicon.toString().toUpperCase() ? a(k).addClass("ui-pg-button " + i).append("<div class='ui-pg-div'>" + c.caption + "</div>") : a(k).addClass("ui-pg-button " + i).append("<div class='ui-pg-div'><span class='" + j + " " + c.buttonicon + "'></span>" + c.caption + "</div>"), c.id && a(k).attr("id", c.id), "first" === c.position ? 0 === e.rows[0].cells.length ? a("tr", e).append(k) : a("tr td:eq(0)", e).before(k) : a("tr", e).append(k), a(k, e).attr("title", c.title || "").click(function (b) {
                            return a(this).hasClass(g) || a.isFunction(c.onClickButton) && c.onClickButton.call(f, b), !1
                        }).hover(function () {
                            a(this).hasClass(g) || a(this).addClass(h)
                        }, function () {
                            a(this).removeClass(h)
                        })
                    } else if (e = a(".dropdownmenu", b)[0]) {
                        var
                        l = a(e).val(),
                            m = c.id || a.jgrid.randId(),
                            n = a('<li class="ui-menu-item" role="presentation"><a class="' + i + ' g-menu-item" tabindex="0" role="menuitem" id="' + m + '">' + (c.caption || c.title) + "</a></li>");
                        l && ("first" === c.position ? a("#" + l).prepend(n) : a("#" + l).append(n), a(n).on("click", function (b) {
                            return a(this).hasClass(g) || (a("#" + l).hide(), a.isFunction(c.onClickButton) && c.onClickButton.call(f, b)), !1
                        }).find("a").hover(function () {
                            a(this).hasClass(g) || a(this).addClass(h)
                        }, function () {
                            a(this).removeClass(h)
                        }))
                    }
                }
            })
        },
        navSeparatorAdd: function (b, c) {
            var
            d = this[0].p.styleUI,
                e = a.jgrid.styleUI[d].common;
            return c = a.extend({
                sepclass: "ui-separator",
                sepcontent: "",
                position: "last"
            }, c || {}), this.each(function () {
                if (this.grid) {
                    "string" == typeof
                    b && 0 !== b.indexOf("#") && (b = "#" + a.jgrid.jqID(b));
                    var
                    d, f, g = a(".navtable", b)[0];
                    this.p.storeNavOptions && this.p.navButtons.push([b, c]), g ? (d = "<td class='ui-pg-button " + e.disabled + "' style='width:4px;'><span class='" + c.sepclass + "'></span>" + c.sepcontent + "</td>", "first" === c.position ? 0 === g.rows[0].cells.length ? a("tr", g).append(d) : a("tr td:eq(0)", g).before(d) : a("tr", g).append(d)) : (g = a(".dropdownmenu", b)[0], d = "<li class='ui-menu-item " + e.disabled + "' style='width:100%' role='presentation'><hr class='ui-separator-li'></li>", g && (f = a(g).val()) && ("first" === c.position ? a("#" + f).prepend(d) : a("#" + f).append(d)))
                }
            })
        },
        _buildNavMenu: function (b, c, d, e, f, g, h, i) {
            return this.each(function () {
                var
                j = this,
                    k = a.jgrid.getRegional(j, "nav"),
                    l = j.p.styleUI,
                    m = (a.jgrid.styleUI[l].navigator, a.jgrid.styleUI[l].filter),
                    n = a.jgrid.styleUI[l].common,
                    o = "form_menu_" + a.jgrid.randId(),
                    p = d.navButtonText ? d.navButtonText : k.selectcaption || "Actions",
                    q = "<button class='dropdownmenu " + n.button + "' value='" + o + "'>" + p + "</button>";
                a(b + "_" + d.position, b).append(q);
                var
                r = {
                    themodal: "alertmod_" + this.p.id,
                    modalhead: "alerthd_" + this.p.id,
                    modalcontent: "alertcnt_" + this.p.id
                };
                (function () {
                    var
                    b, k, l = a(".ui-jqgrid-view").css("font-size") || "11px",
                        p = a('<ul id="' + o + '" class="ui-nav-menu modal-content" role="menu" tabindex="0" style="display:none;font-size:' + l + '"></ul>');
                    d.add && (f = f || {}, b = f.id || "add_" + c, k = a('<li class="ui-menu-item" role="presentation"><a class="' + n.cornerall + ' g-menu-item" tabindex="0" role="menuitem" id="' + b + '">' + (d.addtext || d.addtitle) + "</a></li>").click(function () {
                        return a(this).hasClass(n.disabled) || (a.isFunction(d.addfunc) ? d.addfunc.call(j) : a(j).jqGrid("editGridRow", "new", f), a(p).hide()), !1
                    }), a(p).append(k)), d.edit && (e = e || {}, b = e.id || "edit_" + c, k = a('<li class="ui-menu-item" role="presentation"><a class="' + n.cornerall + ' g-menu-item" tabindex="0" role="menuitem" id="' + b + '">' + (d.edittext || d.edittitle) + "</a></li>").click(function () {
                        if (!a(this).hasClass(n.disabled)) {
                            var
                            b = j.p.selrow;
                            b ? a.isFunction(d.editfunc) ? d.editfunc.call(j, b) : a(j).jqGrid("editGridRow", b, e) : (a.jgrid.viewModal("#" + r.themodal, {
                                gbox: "#gbox_" + a.jgrid.jqID(j.p.id),
                                jqm: !0
                            }), a("#jqg_alrt").focus()), a(p).hide()
                        }
                        return !1
                    }), a(p).append(k)), d.view && (i = i || {}, b = i.id || "view_" + c, k = a('<li class="ui-menu-item" role="presentation"><a class="' + n.cornerall + ' g-menu-item" tabindex="0" role="menuitem" id="' + b + '">' + (d.viewtext || d.viewtitle) + "</a></li>").click(function () {
                        if (!a(this).hasClass(n.disabled)) {
                            var
                            b = j.p.selrow;
                            b ? a.isFunction(d.editfunc) ? d.viewfunc.call(j, b) : a(j).jqGrid("viewGridRow", b, i) : (a.jgrid.viewModal("#" + r.themodal, {
                                gbox: "#gbox_" + a.jgrid.jqID(j.p.id),
                                jqm: !0
                            }), a("#jqg_alrt").focus()), a(p).hide()
                        }
                        return !1
                    }), a(p).append(k)), d.del && (g = g || {}, b = g.id || "del_" + c, k = a('<li class="ui-menu-item" role="presentation"><a class="' + n.cornerall + ' g-menu-item" tabindex="0" role="menuitem" id="' + b + '">' + (d.deltext || d.deltitle) + "</a></li>").click(function () {
                        if (!a(this).hasClass(n.disabled)) {
                            var
                            b;
                            j.p.multiselect ? (b = j.p.selarrrow, 0 === b.length && (b = null)) : b = j.p.selrow, b ? a.isFunction(d.delfunc) ? d.delfunc.call(j, b) : a(j).jqGrid("delGridRow", b, g) : (a.jgrid.viewModal("#" + r.themodal, {
                                gbox: "#gbox_" + a.jgrid.jqID(j.p.id),
                                jqm: !0
                            }), a("#jqg_alrt").focus()), a(p).hide()
                        }
                        return !1
                    }), a(p).append(k)), (d.add || d.edit || d.del || d.view) && a(p).append("<li class='ui-menu-item " + n.disabled + "' style='width:100%' role='presentation'><hr class='ui-separator-li'></li>"), d.search && (h = h || {}, b = h.id || "search_" + c, k = a('<li class="ui-menu-item" role="presentation"><a class="' + n.cornerall + ' g-menu-item" tabindex="0" role="menuitem" id="' + b + '">' + (d.searchtext || d.searchtitle) + "</a></li>").click(function () {
                        return a(this).hasClass(n.disabled) || (a.isFunction(d.searchfunc) ? d.searchfunc.call(j, h) : a(j).jqGrid("searchGrid", h), a(p).hide()), !1
                    }), a(p).append(k), h.showOnLoad && !0 === h.showOnLoad && a(k).click()), d.refresh && (b = h.id || "search_" + c, k = a('<li class="ui-menu-item" role="presentation"><a class="' + n.cornerall + ' g-menu-item" tabindex="0" role="menuitem" id="' + b + '">' + (d.refreshtext || d.refreshtitle) + "</a></li>").click(function () {
                        if (!a(this).hasClass(n.disabled)) {
                            a.isFunction(d.beforeRefresh) && d.beforeRefresh.call(j), j.p.search = !1, j.p.resetsearch = !0;
                            try {
                                if ("currentfilter" !== d.refreshstate) {
                                    var
                                    b = j.p.id;
                                    j.p.postData.filters = "";
                                    try {
                                        a("#fbox_" + a.jgrid.jqID(b)).jqFilter("resetFilter")
                                    } catch (a) {}
                                    a.isFunction(j.clearToolbar) && j.clearToolbar.call(j, !1)
                                }
                            } catch (a) {}
                            switch (d.refreshstate) {
                                case "firstpage":
                                    a(j).trigger("reloadGrid", [{
                                        page: 1
                                    }]);
                                    break;
                                case "current":
                                case "currentfilter":
                                    a(j).trigger("reloadGrid", [{
                                        current: !0
                                    }])
                            }
                            a.isFunction(d.afterRefresh) && d.afterRefresh.call(j), a(p).hide()
                        }
                        return !1
                    }), a(p).append(k)), a(p).hide(), a("body").append(p), a("#" + o).addClass("ui-menu " + m.menu_widget), a("#" + o + " > li > a").hover(function () {
                        a(this).addClass(n.hover)
                    }, function () {
                        a(this).removeClass(n.hover)
                    })
                })(), a(".dropdownmenu", b + "_" + d.position).on("click", function (b) {
                    var
                    c = a(this).offset(),
                        d = c.left,
                        e = parseInt(c.top),
                        f = a(this).val();
                    a("#" + f).show().css({
                        top: e - (a("#" + f).height() + 10) + "px",
                        left: d + "px"
                    }), b.stopPropagation()
                }), a("body").on("click", function (b) {
                    a(b.target).hasClass("dropdownmenu") || a("#" + o).hide()
                })
            })
        },
        GridToForm: function (b, c) {
            return this.each(function () {
                var
                d, e = this;
                if (e.grid) {
                    var
                    f = a(e).jqGrid("getRowData", b);
                    if (f) for (d in f) f.hasOwnProperty(d) && (a("[name=" + a.jgrid.jqID(d) + "]", c).is("input:radio") || a("[name=" + a.jgrid.jqID(d) + "]", c).is("input:checkbox") ? a("[name=" + a.jgrid.jqID(d) + "]", c).each(function () {
                        a(this).val() == f[d] ? a(this)[e.p.useProp ? "prop" : "attr"]("checked", !0) : a(this)[e.p.useProp ? "prop" : "attr"]("checked", !1)
                    }) : a("[name=" + a.jgrid.jqID(d) + "]", c).val(f[d]))
                }
            })
        },
        FormToGrid: function (b, c, d, e) {
            return this.each(function () {
                var
                f = this;
                if (f.grid) {
                    d || (d = "set"), e || (e = "first");
                    var
                    g = a(c).serializeArray(),
                        h = {};
                    a.each(g, function (a, b) {
                        h[b.name] = b.value
                    }), "add" === d ? a(f).jqGrid("addRowData", b, h, e) : "set" === d && a(f).jqGrid("setRowData", b, h)
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "./grid.common"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.fn.jqFilter = function (b) {
        if ("string" == typeof
        b) {
            var
            c = a.fn.jqFilter[b];
            if (!c) throw "jqFilter - No such method: " + b;
            var
            d = a.makeArray(arguments).slice(1);
            return c.apply(this, d)
        }
        var
        e = a.extend(!0, {
            filter: null,
            columns: [],
            sortStrategy: null,
            onChange: null,
            afterRedraw: null,
            checkValues: null,
            error: !1,
            errmsg: "",
            errorcheck: !0,
            showQuery: !0,
            sopt: null,
            ops: [],
            operands: null,
            numopts: ["eq", "ne", "lt", "le", "gt", "ge", "nu", "nn", "in", "ni"],
            stropts: ["eq", "ne", "bw", "bn", "ew", "en", "cn", "nc", "nu", "nn", "in", "ni"],
            strarr: ["text", "string", "blob"],
            groupOps: [{
                op: "AND",
                text: "AND"
            }, {
                op: "OR",
                text: "OR"
            }],
            groupButton: !0,
            ruleButtons: !0,
            uniqueSearchFields: !1,
            direction: "ltr",
            addsubgrup: "Add subgroup",
            addrule: "Add rule",
            delgroup: "Delete group",
            delrule: "Delete rule",
            autoencode: !1
        }, a.jgrid.filter, b || {});
        return this.each(function () {
            if (!this.filter) {
                this.p = e, null !== this.p.filter && void
                0 !== this.p.filter || (this.p.filter = {
                    groupOp: this.p.groupOps[0].op,
                    rules: [],
                    groups: []
                }), null != this.p.sortStrategy && a.isFunction(this.p.sortStrategy) && this.p.columns.sort(this.p.sortStrategy);
                var
                b, c, d = this.p.columns.length,
                    f = /msie/i.test(navigator.userAgent) && !window.opera;
                if (this.p.initFilter = a.extend(!0, {}, this.p.filter), d) {
                    for (b = 0; b < d; b++) c = this.p.columns[b], c.stype ? c.inputtype = c.stype : c.inputtype || (c.inputtype = "text"), c.sorttype ? c.searchtype = c.sorttype : c.searchtype || (c.searchtype = "string"), void
                    0 === c.hidden && (c.hidden = !1), c.label || (c.label = c.name), c.index && (c.name = c.index), c.hasOwnProperty("searchoptions") || (c.searchoptions = {}), c.hasOwnProperty("searchrules") || (c.searchrules = {}), void
                    0 === c.search ? c.inlist = !0 : c.inlist = c.search;
                    var
                    g = function () {
                        return a("#" + a.jgrid.jqID(e.id))[0] || null
                    }, h = g(),
                        i = a.jgrid.styleUI[h.p.styleUI || "jQueryUI"].filter,
                        j = a.jgrid.styleUI[h.p.styleUI || "jQueryUI"].common;
                    this.p.showQuery && a(this).append("<table class='queryresult " + i.table_widget + "' style='display:block;max-width:440px;border:0px none;' dir='" + this.p.direction + "'><tbody><tr><td class='query'></td></tr></tbody></table>");
                    var
                    k = function (b, c) {
                        var
                        d = [!0, ""],
                            f = g();
                        if (a.isFunction(c.searchrules)) d = c.searchrules.call(f, b, c);
                        else if (a.jgrid && a.jgrid.checkValues) try {
                            d = a.jgrid.checkValues.call(f, b, -1, c.searchrules, c.label)
                        } catch (a) {}
                        d && d.length && !1 === d[0] && (e.error = !d[0], e.errmsg = d[1])
                    };
                    this.onchange = function () {
                        return this.p.error = !1, this.p.errmsg = "", !! a.isFunction(this.p.onChange) && this.p.onChange.call(this, this.p)
                    }, this.reDraw = function () {
                        a("table.group:first", this).remove();
                        var
                        b = this.createTableForGroup(e.filter, null);
                        a(this).append(b), a.isFunction(this.p.afterRedraw) && this.p.afterRedraw.call(this, this.p)
                    }, this.createTableForGroup = function (b, c) {
                        var
                        d, f = this,
                            g = a("<table class='group " + i.table_widget + " ui-search-table' style='border:0px none;'><tbody></tbody></table>"),
                            h = "left";
                        "rtl" === this.p.direction && (h = "right", g.attr("dir", "rtl")), null === c && g.append("<tr class='error' style='display:none;'><th colspan='5' class='" + j.error + "' align='" + h + "'></th></tr>");
                        var
                        k = a("<tr></tr>");
                        g.append(k);
                        var
                        l = a("<th colspan='5' align='" + h + "'></th>");
                        if (k.append(l), !0 === this.p.ruleButtons) {
                            var
                            m = a("<select class='opsel " + i.srSelect + "'></select>");
                            l.append(m);
                            var
                            n, o = "";
                            for (d = 0; d < e.groupOps.length; d++) n = b.groupOp === f.p.groupOps[d].op ? " selected='selected'" : "", o += "<option value='" + f.p.groupOps[d].op + "'" + n + ">" + f.p.groupOps[d].text + "</option>";
                            m.append(o).on("change", function () {
                                b.groupOp = a(m).val(), f.onchange()
                            })
                        }
                        var
                        p = "<span></span>";
                        if (this.p.groupButton && (p = a("<input type='button' value='+ {}' title='" + f.p.subgroup + "' class='add-group " + j.button + "'/>"), p.on("click", function () {
                            return void
                            0 === b.groups && (b.groups = []), b.groups.push({
                                groupOp: e.groupOps[0].op,
                                rules: [],
                                groups: []
                            }), f.reDraw(), f.onchange(), !1
                        })), l.append(p), !0 === this.p.ruleButtons) {
                            var
                            q, r = a("<input type='button' value='+' title='" + f.p.addrule + "' class='add-rule ui-add " + j.button + "'/>");
                            r.on("click", function () {
                                for (void
                                0 === b.rules && (b.rules = []), d = 0; d < f.p.columns.length; d++) {
                                    var
                                    c = void
                                    0 === f.p.columns[d].search || f.p.columns[d].search,
                                        e = !0 === f.p.columns[d].hidden;
                                    if (!0 === f.p.columns[d].searchoptions.searchhidden && c || c && !e) {
                                        q = f.p.columns[d];
                                        break
                                    }
                                }
                                if (!q) return !1;
                                var
                                g;
                                return g = q.searchoptions.sopt ? q.searchoptions.sopt : f.p.sopt ? f.p.sopt : -1 !== a.inArray(q.searchtype, f.p.strarr) ? f.p.stropts : f.p.numopts, b.rules.push({
                                    field: q.name,
                                    op: g[0],
                                    data: ""
                                }), f.reDraw(), !1
                            }), l.append(r)
                        }
                        if (null !== c) {
                            var
                            s = a("<input type='button' value='-' title='" + f.p.delgroup + "' class='delete-group " + j.button + "'/>");
                            l.append(s), s.on("click", function () {
                                for (d = 0; d < c.groups.length; d++) if (c.groups[d] === b) {
                                    c.groups.splice(d, 1);
                                    break
                                }
                                return f.reDraw(), f.onchange(), !1
                            })
                        }
                        if (void
                        0 !== b.groups) for (d = 0; d < b.groups.length; d++) {
                            var
                            t = a("<tr></tr>");
                            g.append(t);
                            var
                            u = a("<td class='first'></td>");
                            t.append(u);
                            var
                            v = a("<td colspan='4'></td>");
                            v.append(this.createTableForGroup(b.groups[d], b)), t.append(v)
                        }
                        void
                        0 === b.groupOp && (b.groupOp = f.p.groupOps[0].op);
                        var
                        w, x = f.p.ruleButtons && f.p.uniqueSearchFields;
                        if (x) for (w = 0; w < f.p.columns.length; w++) f.p.columns[w].inlist && (f.p.columns[w].search = !0);
                        if (void
                        0 !== b.rules) for (d = 0; d < b.rules.length; d++) if (g.append(this.createTableRowForRule(b.rules[d], b)), x) {
                            var
                            y = b.rules[d].field;
                            for (w = 0; w < f.p.columns.length; w++) if (y === f.p.columns[w].name) {
                                f.p.columns[w].search = !1;
                                break
                            }
                        }
                        return g
                    }, this.createTableRowForRule = function (b, c) {
                        var
                        d, h, k, l, m, n = this,
                            o = g(),
                            p = a("<tr></tr>"),
                            q = "";
                        p.append("<td class='first'></td>");
                        var
                        r = a("<td class='columns'></td>");
                        p.append(r);
                        var
                        s, t = a("<select class='" + i.srSelect + "'></select>"),
                            u = [];
                        r.append(t), t.on("change", function () {
                            if (n.p.ruleButtons && n.p.uniqueSearchFields) {
                                var
                                c = parseInt(a(this).data("curr"), 10),
                                    e = this.selectedIndex;
                                c >= 0 && (n.p.columns[c].search = !0, a(this).data("curr", e), n.p.columns[e].search = !1)
                            }
                            for (b.field = a(t).val(), k = a(this).parents("tr:first"), a(".data", k).empty(), d = 0; d < n.p.columns.length; d++) if (n.p.columns[d].name === b.field) {
                                l = n.p.columns[d];
                                break
                            }
                            if (l) {
                                l.searchoptions.id = a.jgrid.randId(), l.searchoptions.name = b.field, l.searchoptions.oper = "filter", f && "text" === l.inputtype && (l.searchoptions.size || (l.searchoptions.size = 10));
                                var
                                g = a.jgrid.createEl.call(o, l.inputtype, l.searchoptions, "", !0, n.p.ajaxSelectOptions || {}, !0);
                                a(g).addClass("input-elm " + i.srInput), h = l.searchoptions.sopt ? l.searchoptions.sopt : n.p.sopt ? n.p.sopt : -1 !== a.inArray(l.searchtype, n.p.strarr) ? n.p.stropts : n.p.numopts;
                                var
                                j = "",
                                    m = 0;
                                for (u = [], a.each(n.p.ops, function () {
                                    u.push(this.oper)
                                }), d = 0; d < h.length; d++) - 1 !== (s = a.inArray(h[d], u)) && (0 === m && (b.op = n.p.ops[s].oper), j += "<option value='" + n.p.ops[s].oper + "'>" + n.p.ops[s].text + "</option>", m++);
                                if (a(".selectopts", k).empty().append(j), a(".selectopts", k)[0].selectedIndex = 0, a.jgrid.msie() && a.jgrid.msiever() < 9) {
                                    var
                                    p = parseInt(a("select.selectopts", k)[0].offsetWidth, 10) + 1;
                                    a(".selectopts", k).width(p), a(".selectopts", k).css("width", "auto")
                                }
                                a(".data", k).append(g), a.jgrid.bindEv.call(o, g, l.searchoptions), a(".input-elm", k).on("change", function (c) {
                                    var
                                    d = c.target;
                                    "custom" === l.inputtype && a.isFunction(l.searchoptions.custom_value) ? b.data = l.searchoptions.custom_value.call(o, a(".customelement", this), "get") : b.data = a(d).val(), "select" === l.inputtype && l.searchoptions.multiple && (b.data = b.data.join(",")), n.onchange()
                                }), setTimeout(function () {
                                    b.data = a(g).val(), n.onchange()
                                }, 0)
                            }
                        });
                        var
                        v = 0;
                        for (d = 0; d < n.p.columns.length; d++) {
                            var
                            w = void
                            0 === n.p.columns[d].search || n.p.columns[d].search,
                                x = !0 === n.p.columns[d].hidden;
                            (!0 === n.p.columns[d].searchoptions.searchhidden && w || w && !x) && (m = "", b.field === n.p.columns[d].name && (m = " selected='selected'", v = d), q += "<option value='" + n.p.columns[d].name + "'" + m + ">" + n.p.columns[d].label + "</option>")
                        }
                        t.append(q), t.data("curr", v);
                        var
                        y = a("<td class='operators'></td>");
                        p.append(y), l = e.columns[v], l.searchoptions.id = a.jgrid.randId(), f && "text" === l.inputtype && (l.searchoptions.size || (l.searchoptions.size = 10)), l.searchoptions.name = b.field, l.searchoptions.oper = "filter";
                        var
                        z = a.jgrid.createEl.call(o, l.inputtype, l.searchoptions, b.data, !0, n.p.ajaxSelectOptions || {}, !0);
                        "nu" !== b.op && "nn" !== b.op || (a(z).attr("readonly", "true"), a(z).attr("disabled", "true"));
                        var
                        A = a("<select class='selectopts " + i.srSelect + "'></select>");
                        for (y.append(A), A.on("change", function () {
                            b.op = a(A).val(), k = a(this).parents("tr:first");
                            var
                            c = a(".input-elm", k)[0];
                            "nu" === b.op || "nn" === b.op ? (b.data = "", "SELECT" !== c.tagName.toUpperCase() && (c.value = ""), c.setAttribute("readonly", "true"), c.setAttribute("disabled", "true")) : ("SELECT" === c.tagName.toUpperCase() && (b.data = c.value), c.removeAttribute("readonly"), c.removeAttribute("disabled")), n.onchange()
                        }), h = l.searchoptions.sopt ? l.searchoptions.sopt : n.p.sopt ? n.p.sopt : -1 !== a.inArray(l.searchtype, n.p.strarr) ? n.p.stropts : n.p.numopts, q = "", a.each(n.p.ops, function () {
                            u.push(this.oper)
                        }), d = 0; d < h.length; d++) - 1 !== (s = a.inArray(h[d], u)) && (m = b.op === n.p.ops[s].oper ? " selected='selected'" : "", q += "<option value='" + n.p.ops[s].oper + "'" + m + ">" + n.p.ops[s].text + "</option>");
                        A.append(q);
                        var
                        B = a("<td class='data'></td>");
                        p.append(B), B.append(z), a.jgrid.bindEv.call(o, z, l.searchoptions), a(z).addClass("input-elm " + i.srInput).on("change", function () {
                            b.data = "custom" === l.inputtype ? l.searchoptions.custom_value.call(o, a(".customelement", this), "get") : a(this).val(), n.onchange()
                        });
                        var
                        C = a("<td></td>");
                        if (p.append(C), !0 === this.p.ruleButtons) {
                            var
                            D = a("<input type='button' value='-' title='" + n.p.delrule + "' class='delete-rule ui-del " + j.button + "'/>");
                            C.append(D), D.on("click", function () {
                                for (d = 0; d < c.rules.length; d++) if (c.rules[d] === b) {
                                    c.rules.splice(d, 1);
                                    break
                                }
                                return n.reDraw(), n.onchange(), !1
                            })
                        }
                        return p
                    }, this.getStringForGroup = function (a) {
                        var
                        b, c = "(";
                        if (void
                        0 !== a.groups) for (b = 0; b < a.groups.length; b++) {
                            c.length > 1 && (c += " " + a.groupOp + " ");
                            try {
                                c += this.getStringForGroup(a.groups[b])
                            } catch (a) {
                                alert(a)
                            }
                        }
                        if (void
                        0 !== a.rules) try {
                            for (b = 0; b < a.rules.length; b++) c.length > 1 && (c += " " + a.groupOp + " "), c += this.getStringForRule(a.rules[b])
                        } catch (a) {
                            alert(a)
                        }
                        return c += ")", "()" === c ? "" : c
                    }, this.getStringForRule = function (b) {
                        var
                        c, d, f, g = "",
                            h = "",
                            i = ["int", "integer", "float", "number", "currency"];
                        for (c = 0; c < this.p.ops.length; c++) if (this.p.ops[c].oper === b.op) {
                            g = this.p.operands.hasOwnProperty(b.op) ? this.p.operands[b.op] : "", h = this.p.ops[c].oper;
                            break
                        }
                        for (c = 0; c < this.p.columns.length; c++) if (this.p.columns[c].name === b.field) {
                            d = this.p.columns[c];
                            break
                        }
                        return void
                        0 === d ? "" : (f = this.p.autoencode ? a.jgrid.htmlEncode(b.data) : b.data, "bw" !== h && "bn" !== h || (f += "%"), "ew" !== h && "en" !== h || (f = "%" + f), "cn" !== h && "nc" !== h || (f = "%" + f + "%"), "in" !== h && "ni" !== h || (f = " (" + f + ")"), e.errorcheck && k(b.data, d), -1 !== a.inArray(d.searchtype, i) || "nn" === h || "nu" === h ? b.field + " " + g + " " + f : b.field + " " + g + ' "' + f + '"')
                    }, this.resetFilter = function () {
                        this.p.filter = a.extend(!0, {}, this.p.initFilter), this.reDraw(), this.onchange()
                    }, this.hideError = function () {
                        a("th." + j.error, this).html(""), a("tr.error", this).hide()
                    }, this.showError = function () {
                        a("th." + j.error, this).html(this.p.errmsg), a("tr.error", this).show()
                    }, this.toUserFriendlyString = function () {
                        return this.getStringForGroup(e.filter)
                    }, this.toString = function () {
                        function
                        a(a) {
                            if (c.p.errorcheck) {
                                var
                                b, d;
                                for (b = 0; b < c.p.columns.length; b++) if (c.p.columns[b].name === a.field) {
                                    d = c.p.columns[b];
                                    break
                                }
                                d && k(a.data, d)
                            }
                            return a.op + "(item." + a.field + ",'" + a.data + "')"
                        }

                        function
                        b(c) {
                            var
                            d, e = "(";
                            if (void
                            0 !== c.groups) for (d = 0; d < c.groups.length; d++) e.length > 1 && ("OR" === c.groupOp ? e += " || " : e += " && "), e += b(c.groups[d]);
                            if (void
                            0 !== c.rules) for (d = 0; d < c.rules.length; d++) e.length > 1 && ("OR" === c.groupOp ? e += " || " : e += " && "), e += a(c.rules[d]);
                            return e += ")", "()" === e ? "" : e
                        }
                        var
                        c = this;
                        return b(this.p.filter)
                    }, this.reDraw(), this.p.showQuery && this.onchange(), this.filter = !0
                }
            }
        })
    }, a.extend(a.fn.jqFilter, {
        toSQLString: function () {
            var
            a = "";
            return this.each(function () {
                a = this.toUserFriendlyString()
            }), a
        },
        filterData: function () {
            var
            a;
            return this.each(function () {
                a = this.p.filter
            }), a
        },
        getParameter: function (a) {
            return void
            0 !== a && this.p.hasOwnProperty(a) ? this.p[a] : this.p
        },
        resetFilter: function () {
            return this.each(function () {
                this.resetFilter()
            })
        },
        addFilter: function (b) {
            "string" == typeof
            b && (b = a.jgrid.parse(b)), this.each(function () {
                this.p.filter = b, this.reDraw(), this.onchange()
            })
        }
    }), a.extend(a.jgrid, {
        filterRefactor: function (b) {
            var
            c, d, e, f, g, h = {};
            try {
                if (h = "string" == typeof
                b.ruleGroudp ? a.jgrid.parse(b.ruleGroup) : b.ruleGroup, h.rules && h.rules.length) for (c = h.rules, d = 0; d < c.length; d++) e = c[d], a.inArray(e.filed, b.ssfield) && (f = e.data.split(b.splitSelect), f.length > 1 && (void
                0 === h.groups && (h.groups = []), g = {
                    groupOp: b.groupOpSelect,
                    groups: [],
                    rules: []
                }, h.groups.push(g), a.each(f, function (a) {
                    f[a] && g.rules.push({
                        data: f[a],
                        op: e.op,
                        field: e.field
                    })
                }), c.splice(d, 1), d--))
            } catch (a) {}
            return h
        }
    }), a.jgrid.extend({
        filterToolbar: function (b) {
            var
            c = a.jgrid.getRegional(this[0], "search");
            return b = a.extend({
                autosearch: !0,
                autosearchDelay: 500,
                searchOnEnter: !0,
                beforeSearch: null,
                afterSearch: null,
                beforeClear: null,
                afterClear: null,
                onClearSearchValue: null,
                url: "",
                stringResult: !1,
                groupOp: "AND",
                defaultSearch: "bw",
                searchOperators: !1,
                resetIcon: "x",
                splitSelect: ",",
                groupOpSelect: "OR",
                operands: {
                    eq: "==",
                    ne: "!",
                    lt: "<",
                    le: "<=",
                    gt: ">",
                    ge: ">=",
                    bw: "^",
                    bn: "!^",
                    in : "=",
                    ni: "!=",
                    ew: "|",
                    en: "!@",
                    cn: "~",
                    nc: "!~",
                    nu: "#",
                    nn: "!#",
                    bt: "..."
                }
            }, c, b || {}), this.each(function () {
                var
                d = this;
                if (!d.p.filterToolbar) {
                    a(d).data("filterToolbar") || a(d).data("filterToolbar", b), d.p.force_regional && (b = a.extend(b, c));
                    var
                    e, f, g, h = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].filter,
                        i = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].common,
                        j = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].base,
                        k = function () {
                            var
                            c, e, f, g, h = {}, i = 0,
                                j = {}, k = !1,
                                l = [],
                                m = !1;
                            a.each(d.p.colModel, function () {
                                var
                                n = a("#gs_" + d.p.idPrefix + a.jgrid.jqID(this.name), !0 === this.frozen && !0 === d.p.frozenColumns ? d.grid.fhDiv : d.grid.hDiv);
                                if (e = this.index || this.name, g = this.searchoptions || {}, f = b.searchOperators && g.searchOperMenu ? n.parent().prev().children("a").attr("soper") || b.defaultSearch : g.sopt ? g.sopt[0] : "select" === this.stype ? "eq" : b.defaultSearch, c = "custom" === this.stype && a.isFunction(g.custom_value) && n.length > 0 ? g.custom_value.call(d, n, "get") : n.val(), "select" === this.stype && g.multiple && a.isArray(c) && c.length && (k = !0, l.push(e), c = 1 === c.length ? c[0] : c), "bt" === f && (m = !0), c || "nu" === f || "nn" === f) h[e] = c, j[e] = f, i++;
                                else try {
                                    delete
                                    d.p.postData[e]
                                } catch (a) {}
                            });
                            var
                            n = i > 0;
                            if (!0 === b.stringResult || "local" === d.p.datatype || !0 === b.searchOperators) {
                                var
                                o = '{"groupOp":"' + b.groupOp + '","rules":[',
                                    p = 0;
                                a.each(h, function (a, b) {
                                    p > 0 && (o += ","), o += '{"field":"' + a + '",', o += '"op":"' + j[a] + '",', b += "", o += '"data":"' + b.replace(/\\/g, "\\\\").replace(/\"/g, '\\"') + '"}', p++
                                }), o += "]}";
                                var
                                q, r, s, t, u, v, w;
                                if (k && a.jgrid.filterRefactor({
                                    ruleGroup: o,
                                    ssfield: l,
                                    splitSelect: b.splitSelect,
                                    groupOpSelect: b.groupOpSelect
                                }), m && (a.isPlainObject(q) || (q = a.jgrid.parse(o)), q.rules && q.rules.length)) for (r = q.rules, s = 0; s < r.length; s++) u = r[s], "bt" === u.op && (v = u.data.split("..."), v.length > 1 && (void
                                0 === q.groups && (q.groups = []), w = {
                                    groupOp: "AND",
                                    groups: [],
                                    rules: []
                                }, q.groups.push(w), a.each(v, function (a) {
                                    var
                                    b = 0 === a ? "ge" : "le";
                                    (t = v[a]) && w.rules.push({
                                        data: v[a],
                                        op: b,
                                        field: u.field
                                    })
                                }), r.splice(s, 1), s--));
                                (m || k) && (o = JSON.stringify(q)), a.extend(d.p.postData, {
                                    filters: o
                                }), a.each(["searchField", "searchString", "searchOper"], function (a, b) {
                                    d.p.postData.hasOwnProperty(b) && delete
                                    d.p.postData[b]
                                })
                            } else a.extend(d.p.postData, h);
                            var
                            x;
                            b.url && (x = d.p.url, a(d).jqGrid("setGridParam", {
                                url: b.url
                            }));
                            var
                            y = "stop" === a(d).triggerHandler("jqGridToolbarBeforeSearch");
                            !y && a.isFunction(b.beforeSearch) && (y = b.beforeSearch.call(d)), y || a(d).jqGrid("setGridParam", {
                                search: n
                            }).trigger("reloadGrid", [{
                                page: 1
                            }]), x && a(d).jqGrid("setGridParam", {
                                url: x
                            }), a(d).triggerHandler("jqGridToolbarAfterSearch"), a.isFunction(b.afterSearch) && b.afterSearch.call(d)
                        }, l = function (c) {
                            var
                            e, f = {}, g = 0;
                            c = "boolean" != typeof
                            c || c, a.each(d.p.colModel, function () {
                                var
                                b, c = a("#gs_" + d.p.idPrefix + a.jgrid.jqID(this.name), !0 === this.frozen && !0 === d.p.frozenColumns ? d.grid.fhDiv : d.grid.hDiv);
                                switch (this.searchoptions && void
                                0 !== this.searchoptions.defaultValue && (b = this.searchoptions.defaultValue), e = this.index || this.name, this.stype) {
                                    case "select":
                                        if (c.find("option").each(function (c) {
                                            if (0 === c && (this.selected = !0), a(this).val() === b) return this.selected = !0, !1
                                        }), void
                                        0 !== b) f[e] = b, g++;
                                        else try {
                                            delete
                                            d.p.postData[e]
                                        } catch (a) {}
                                        break;
                                    case "text":
                                        if (c.val(b || ""), void
                                        0 !== b) f[e] = b, g++;
                                        else try {
                                            delete
                                            d.p.postData[e]
                                        } catch (a) {}
                                        break;
                                    case "custom":
                                        a.isFunction(this.searchoptions.custom_value) && c.length > 0 && this.searchoptions.custom_value.call(d, c, "set", b || "")
                                }
                            });
                            var
                            h = g > 0;
                            if (d.p.resetsearch = !0, !0 === b.stringResult || "local" === d.p.datatype) {
                                var
                                i = '{"groupOp":"' + b.groupOp + '","rules":[',
                                    j = 0;
                                a.each(f, function (a, b) {
                                    j > 0 && (i += ","), i += '{"field":"' + a + '",', i += '"op":"eq",', b += "", i += '"data":"' + b.replace(/\\/g, "\\\\").replace(/\"/g, '\\"') + '"}', j++
                                }), i += "]}", a.extend(d.p.postData, {
                                    filters: i
                                }), a.each(["searchField", "searchString", "searchOper"], function (a, b) {
                                    d.p.postData.hasOwnProperty(b) && delete
                                    d.p.postData[b]
                                })
                            } else a.extend(d.p.postData, f);
                            var
                            k;
                            b.url && (k = d.p.url, a(d).jqGrid("setGridParam", {
                                url: b.url
                            }));
                            var
                            l = "stop" === a(d).triggerHandler("jqGridToolbarBeforeClear");
                            !l && a.isFunction(b.beforeClear) && (l = b.beforeClear.call(d)), l || c && a(d).jqGrid("setGridParam", {
                                search: h
                            }).trigger("reloadGrid", [{
                                page: 1
                            }]), k && a(d).jqGrid("setGridParam", {
                                url: k
                            }), a(d).triggerHandler("jqGridToolbarAfterClear"), a.isFunction(b.afterClear) && b.afterClear()
                        }, m = function () {
                            var
                            b = a("tr.ui-search-toolbar", d.grid.hDiv);
                            !0 === d.p.frozenColumns && a(d).jqGrid("destroyFrozenColumns"), "none" === b.css("display") ? b.show() : b.hide(), !0 === d.p.frozenColumns && a(d).jqGrid("setFrozenColumns")
                        }, n = function (c, e, f) {
                            a("#sopt_menu").remove(), e = parseInt(e, 10), f = parseInt(f, 10) + 18;
                            for (var
                            g, j, l = a(".ui-jqgrid-view").css("font-size") || "11px", m = '<ul id="sopt_menu" class="ui-search-menu modal-content" role="menu" tabindex="0" style="font-size:' + l + ";left:" + e + "px;top:" + f + 'px;">', n = a(c).attr("soper"), o = [], p = 0, q = a(c).attr("colname"), r = d.p.colModel.length; p < r && d.p.colModel[p].name !== q;) p++;
                            var
                            s = d.p.colModel[p],
                                t = a.extend({}, s.searchoptions);
                            for (t.sopt || (t.sopt = [], t.sopt[0] = "select" === s.stype ? "eq" : b.defaultSearch), a.each(b.odata, function () {
                                o.push(this.oper)
                            }), p = 0; p < t.sopt.length; p++) - 1 !== (j = a.inArray(t.sopt[p], o)) && (g = n === b.odata[j].oper ? i.highlight : "", m += '<li class="ui-menu-item ' + g + '" role="presentation"><a class="' + i.cornerall + ' g-menu-item" tabindex="0" role="menuitem" value="' + b.odata[j].oper + '" oper="' + b.operands[b.odata[j].oper] + '"><table class="ui-common-table"><tr><td width="25px">' + b.operands[b.odata[j].oper] + "</td><td>" + b.odata[j].text + "</td></tr></table></a></li>");
                            m += "</ul>", a("body").append(m), a("#sopt_menu").addClass("ui-menu " + h.menu_widget), a("#sopt_menu > li > a").hover(function () {
                                a(this).addClass(i.hover)
                            }, function () {
                                a(this).removeClass(i.hover)
                            }).click(function () {
                                var
                                e = a(this).attr("value"),
                                    f = a(this).attr("oper");
                                if (a(d).triggerHandler("jqGridToolbarSelectOper", [e, f, c]), a("#sopt_menu").hide(), a(c).text(f).attr("soper", e), !0 === b.autosearch) {
                                    var
                                    g = a(c).parent().next().children()[0];
                                    (a(g).val() || "nu" === e || "nn" === e) && k()
                                }
                            })
                        }, o = a("<tr class='ui-search-toolbar' role='row'></tr>");
                    b.restoreFromFilters && (g = d.p.postData.filters) && ("string" == typeof
                    g && (g = a.jgrid.parse(g)), f = !! g.rules.length && g.rules), a.each(d.p.colModel, function (c) {
                        var
                        g, i, l, m, n, p, q, r, s = this,
                            t = "",
                            u = "=",
                            v = a("<th role='columnheader' class='" + j.headerBox + " ui-th-" + d.p.direction + "' id='gsh_" + d.p.id + "_" + s.name + "' ></th>"),
                            w = a("<div></div>"),
                            x = a("<table class='ui-search-table' cellspacing='0'><tr><td class='ui-search-oper' headers=''></td><td class='ui-search-input' headers=''></td><td class='ui-search-clear' headers=''></td></tr></table>");
                        if (!0 === this.hidden && a(v).css("display", "none"), this.search = !1 !== this.search, void
                        0 === this.stype && (this.stype = "text"), this.searchoptions = this.searchoptions || {}, void
                        0 === this.searchoptions.searchOperMenu && (this.searchoptions.searchOperMenu = !0), g = a.extend({}, this.searchoptions, {
                            name: s.index || s.name,
                            id: "gs_" + d.p.idPrefix + s.name,
                            oper: "search"
                        }), this.search) {
                            if (b.restoreFromFilters && f) {
                                r = !1;
                                for (var
                                y = 0; y < f.length; y++) if (f[y].field) {
                                    var
                                    z = s.index || s.name;
                                    if (z === f[y].field) {
                                        r = f[y];
                                        break
                                    }
                                }
                            }
                            if (b.searchOperators) {
                                for (i = g.sopt ? g.sopt[0] : "select" === s.stype ? "eq" : b.defaultSearch, b.restoreFromFilters && r && (i = r.op), l = 0; l < b.odata.length; l++) if (b.odata[l].oper === i) {
                                    u = b.operands[i] || "";
                                    break
                                }
                                m = null != g.searchtitle ? g.searchtitle : b.operandTitle, t = this.searchoptions.searchOperMenu ? "<a title='" + m + "' style='padding-right: 0.5em;' soper='" + i + "' class='soptclass' colname='" + this.name + "'>" + u + "</a>" : ""
                            }
                            switch (a("td:eq(0)", x).attr("colindex", c).append(t), void
                            0 === g.clearSearch && (g.clearSearch = !0), g.clearSearch ? (n = b.resetTitle || "Clear Search Value", a("td:eq(2)", x).append("<a title='" + n + "' style='padding-right: 0.3em;padding-left: 0.3em;' class='clearsearchclass'>" + b.resetIcon + "</a>")) : a("td:eq(2)", x).hide(), this.surl && (g.dataUrl = this.surl), p = "", g.defaultValue && (p = a.isFunction(g.defaultValue) ? g.defaultValue.call(d) : g.defaultValue), b.restoreFromFilters && r && (p = r.data), q = a.jgrid.createEl.call(d, this.stype, g, p, !1, a.extend({}, a.jgrid.ajaxOptions, d.p.ajaxSelectOptions || {})), a(q).addClass(h.srInput), a("td:eq(1)", x).append(q), a(w).append(x), null == g.dataEvents && (g.dataEvents = []), this.stype) {
                                case "select":
                                    !0 === b.autosearch && g.dataEvents.push({
                                        type: "change",
                                        fn: function () {
                                            return k(), !1
                                        }
                                    });
                                    break;
                                case "text":
                                    !0 === b.autosearch && (b.searchOnEnter ? g.dataEvents.push({
                                        type: "keypress",
                                        fn: function (a) {
                                            return 13 === (a.charCode || a.keyCode || 0) ? (k(), !1) : this
                                        }
                                    }) : g.dataEvents.push({
                                        type: "keydown",
                                        fn: function (a) {
                                            switch (a.which) {
                                                case
                                                13:
                                                    return !1;
                                                case
                                                9:
                                                case
                                                16:
                                                case
                                                37:
                                                case
                                                38:
                                                case
                                                39:
                                                case
                                                40:
                                                case
                                                27:
                                                    break;
                                                default:
                                                    e && clearTimeout(e), e = setTimeout(function () {
                                                        k()
                                                    }, b.autosearchDelay)
                                            }
                                        }
                                    }))
                            }
                            a.jgrid.bindEv.call(d, q, g)
                        }
                        a(v).append(w), a(o).append(v), b.searchOperators && "" !== t || a("td:eq(0)", x).hide()
                    }), a("table thead", d.grid.hDiv).append(o), b.searchOperators && (a(".soptclass", o).click(function (b) {
                        var
                        c = a(this).offset(),
                            d = c.left,
                            e = c.top;
                        n(this, d, e), b.stopPropagation()
                    }), a("body").on("click", function (b) {
                        "soptclass" !== b.target.className && a("#sopt_menu").remove()
                    })), a(".clearsearchclass", o).click(function () {
                        var
                        c, e = a(this).parents("tr:first"),
                            f = parseInt(a("td.ui-search-oper", e).attr("colindex"), 10),
                            g = a.extend({}, d.p.colModel[f].searchoptions || {}),
                            h = g.defaultValue ? g.defaultValue : "";
                        "select" === d.p.colModel[f].stype ? (c = a("td.ui-search-input select", e), h ? c.val(h) : c[0].selectedIndex = 0) : (c = a("td.ui-search-input input", e), c.val(h)), a(d).triggerHandler("jqGridToolbarClearVal", [c[0], f, g, h]), a.isFunction(b.onClearSearchValue) && b.onClearSearchValue.call(d, c[0], f, g, h), !0 === b.autosearch && k()
                    }), this.p.filterToolbar = !0, this.triggerToolbar = k, this.clearToolbar = l, this.toggleToolbar = m
                }
            })
        },
        destroyFilterToolbar: function () {
            return this.each(function () {
                this.p.filterToolbar && (this.triggerToolbar = null, this.clearToolbar = null, this.toggleToolbar = null, this.p.filterToolbar = !1, a(this.grid.hDiv).find("table thead tr.ui-search-toolbar").remove())
            })
        },
        refreshFilterToolbar: function (b) {
            return b = a.extend(!0, {
                filters: "",
                onClearVal: null,
                onSetVal: null
            }, b || {}), this.each(function () {
                function
                c(f) {
                    if (f && f.rules) {
                        for (g = f.rules, l = g.length, d = 0; d < l; d++) h = g[d], -1 !== (i = a.inArray(h.field, m)) && (e = a("#gs_" + j.p.idPrefix + a.jgrid.jqID(k[i].name)), e.length > 0 && ("select" === k[i].stype ? e.find("option[value='" + a.jgrid.jqID(h.data) + "']").prop("selected", !0) : "text" === k[i].stype && e.val(h.data), a.isFunction(b.onSetVal) && b.onSetVal.call(j, e, k[i].name)));
                        if (f.groups) for (var
                        n = 0; n < f.groups.length; n++) c(f.groups[n])
                    }
                }
                var
                d, e, f, g, h, i, j = this,
                    k = j.p.colModel,
                    l = j.p.colModel.length,
                    m = [];
                if (j.p.filterToolbar) {
                    for (d = 0; d < l; d++) {
                        switch (m.push(k[d].name), e = a("#gs_" + j.p.idPrefix + a.jgrid.jqID(k[d].name)), k[d].stype) {
                            case "select":
                            case "text":
                                e.val("")
                        }
                        a.isFunction(b.onClearVal) && b.onClearVal.call(j, e, k[d].name)
                    }
                    "string" == typeof
                    b.filters && b.filters.length && (f = a.jgrid.parse(b.filters)), a.isPlainObject(f) && c(f)
                }
            })
        },
        searchGrid: function (b) {
            var
            c = a.jgrid.getRegional(this[0], "search");
            return b = a.extend(!0, {
                recreateFilter: !1,
                drag: !0,
                sField: "searchField",
                sValue: "searchString",
                sOper: "searchOper",
                sFilter: "filters",
                loadDefaults: !0,
                beforeShowSearch: null,
                afterShowSearch: null,
                onInitializeSearch: null,
                afterRedraw: null,
                afterChange: null,
                sortStrategy: null,
                closeAfterSearch: !1,
                closeAfterReset: !1,
                closeOnEscape: !1,
                searchOnEnter: !1,
                multipleSearch: !1,
                multipleGroup: !1,
                top: 0,
                left: 0,
                jqModal: !0,
                modal: !1,
                resize: !0,
                width: 450,
                height: "auto",
                dataheight: "auto",
                showQuery: !1,
                errorcheck: !0,
                sopt: null,
                stringResult: void
                0,
                onClose: null,
                onSearch: null,
                onReset: null,
                toTop: !0,
                overlay: 30,
                columns: [],
                tmplNames: null,
                tmplFilters: null,
                tmplLabel: " Template: ",
                showOnLoad: !1,
                layer: null,
                splitSelect: ",",
                groupOpSelect: "OR",
                operands: {
                    eq: "=",
                    ne: "<>",
                    lt: "<",
                    le: "<=",
                    gt: ">",
                    ge: ">=",
                    bw: "LIKE",
                    bn: "NOT LIKE",
                    in : "IN",
                    ni: "NOT IN",
                    ew: "LIKE",
                    en: "NOT LIKE",
                    cn: "LIKE",
                    nc: "NOT LIKE",
                    nu: "IS NULL",
                    nn: "ISNOT NULL"
                }
            }, c, b || {}), this.each(function () {
                function
                c(c) {
                    g = a(d).triggerHandler("jqGridFilterBeforeShow", [c]), void
                    0 === g && (g = !0), g && a.isFunction(b.beforeShowSearch) && (g = b.beforeShowSearch.call(d, c)), g && (a.jgrid.viewModal("#" + a.jgrid.jqID(i.themodal), {
                        gbox: "#gbox_" + a.jgrid.jqID(f),
                        jqm: b.jqModal,
                        modal: b.modal,
                        overlay: b.overlay,
                        toTop: b.toTop
                    }), a(d).triggerHandler("jqGridFilterAfterShow", [c]), a.isFunction(b.afterShowSearch) && b.afterShowSearch.call(d, c))
                }
                var
                d = this;
                if (d.grid) {
                    var
                    e, f = "fbox_" + d.p.id,
                        g = !0,
                        h = !0,
                        i = {
                            themodal: "searchmod" + f,
                            modalhead: "searchhd" + f,
                            modalcontent: "searchcnt" + f,
                            scrollelm: f
                        }, j = a.isPlainObject(d.p_savedFilter) && !a.isEmptyObject(d.p_savedFilter) ? d.p_savedFilter : d.p.postData[b.sFilter],
                        k = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].filter,
                        l = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].common;
                    if (b.styleUI = d.p.styleUI, "string" == typeof
                    j && (j = a.jgrid.parse(j)), !0 === b.recreateFilter && a("#" + a.jgrid.jqID(i.themodal)).remove(), void
                    0 !== a("#" + a.jgrid.jqID(i.themodal))[0]) c(a("#fbox_" + a.jgrid.jqID(d.p.id)));
                    else {
                        var
                        m = a("<div><div id='" + f + "' class='searchFilter' style='overflow:auto'></div></div>").insertBefore("#gview_" + a.jgrid.jqID(d.p.id)),
                            n = "left",
                            o = "";
                        "rtl" === d.p.direction && (n = "right", o = " style='text-align:left'", m.attr("dir", "rtl"));
                        var
                        p, q, r = a.extend([], d.p.colModel),
                            s = "<a id='" + f + "_search' class='fm-button " + l.button + " fm-button-icon-right ui-search'><span class='" + l.icon_base + " " + k.icon_search + "'></span>" + b.Find + "</a>",
                            t = "<a id='" + f + "_reset' class='fm-button " + l.button + " fm-button-icon-left ui-reset'><span class='" + l.icon_base + " " + k.icon_reset + "'></span>" + b.Reset + "</a>",
                            u = "",
                            v = "",
                            w = !1,
                            x = -1,
                            y = !1,
                            z = [];
                        if (b.showQuery && (u = "<a id='" + f + "_query' class='fm-button " + l.button + " fm-button-icon-left'><span class='" + l.icon_base + " " + k.icon_query + "'></span>Query</a>"), b.columns.length ? (r = b.columns, x = 0, p = r[0].index || r[0].name) : a.each(r, function (a, b) {
                            if (b.label || (b.label = d.p.colNames[a]), !w) {
                                var
                                c = void
                                0 === b.search || b.search,
                                    e = !0 === b.hidden;
                                (b.searchoptions && !0 === b.searchoptions.searchhidden && c || c && !e) && (w = !0, p = b.index || b.name, x = a)
                            }
                            "select" === b.stype && b.searchoptions && b.searchoptions.multiple && (y = !0, z.push(b.index || b.name))
                        }), !j && p || !1 === b.multipleSearch) {
                            var
                            A = "eq";
                            x >= 0 && r[x].searchoptions && r[x].searchoptions.sopt ? A = r[x].searchoptions.sopt[0] : b.sopt && b.sopt.length && (A = b.sopt[0]), j = {
                                groupOp: "AND",
                                rules: [{
                                    field: p,
                                    op: A,
                                    data: ""
                                }]
                            }
                        }
                        w = !1, b.tmplNames && b.tmplNames.length && (w = !0, v = "<tr><td class='ui-search-label'>" + b.tmplLabel + "</td>", v += "<td><select class='ui-template " + k.srSelect + "'>", v += "<option value='default'>Default</option>", a.each(b.tmplNames, function (a, b) {
                            v += "<option value='" + a + "'>" + b + "</option>"
                        }), v += "</select></td></tr>"), q = "<table class='EditTable' style='border:0px none;margin-top:5px' id='" + f + "_2'><tbody><tr><td colspan='2'><hr class='" + l.content + "' style='margin:1px'/></td></tr>" + v + "<tr><td class='EditButton' style='text-align:" + n + "'>" + t + "</td><td class='EditButton' " + o + ">" + u + s + "</td></tr></tbody></table>", f = a.jgrid.jqID(f), a("#" + f).jqFilter({
                            columns: r,
                            sortStrategy: b.sortStrategy,
                            filter: b.loadDefaults ? j : null,
                            showQuery: b.showQuery,
                            errorcheck: b.errorcheck,
                            sopt: b.sopt,
                            groupButton: b.multipleGroup,
                            ruleButtons: b.multipleSearch,
                            uniqueSearchFields: b.uniqueSearchFields,
                            afterRedraw: b.afterRedraw,
                            ops: b.odata,
                            operands: b.operands,
                            ajaxSelectOptions: d.p.ajaxSelectOptions,
                            groupOps: b.groupOps,
                            addsubgrup: b.addsubgrup,
                            addrule: b.addrule,
                            delgroup: b.delgroup,
                            delrule: b.delrule,
                            autoencode: d.p.autoencode,
                            onChange: function () {
                                this.p.showQuery && a(".query", this).html(this.toUserFriendlyString()), a.isFunction(b.afterChange) && b.afterChange.call(d, a("#" + f), b)
                            },
                            direction: d.p.direction,
                            id: d.p.id
                        }), m.append(q), w && b.tmplFilters && b.tmplFilters.length && a(".ui-template", m).on("change", function () {
                            var
                            c = a(this).val();
                            return "default" === c ? a("#" + f).jqFilter("addFilter", j) : a("#" + f).jqFilter("addFilter", b.tmplFilters[parseInt(c, 10)]), !1
                        }), !0 === b.multipleGroup && (b.multipleSearch = !0), a(d).triggerHandler("jqGridFilterInitialize", [a("#" + f)]), a.isFunction(b.onInitializeSearch) && b.onInitializeSearch.call(d, a("#" + f)), b.gbox = "#gbox_" + f, b.layer ? a.jgrid.createModal(i, m, b, "#gview_" + a.jgrid.jqID(d.p.id), a("#gbox_" + a.jgrid.jqID(d.p.id))[0], "#" + a.jgrid.jqID(b.layer), {
                            position: "relative"
                        }) : a.jgrid.createModal(i, m, b, "#gview_" + a.jgrid.jqID(d.p.id), a("#gbox_" + a.jgrid.jqID(d.p.id))[0]), (b.searchOnEnter || b.closeOnEscape) && a("#" + a.jgrid.jqID(i.themodal)).keydown(function (c) {
                            var
                            d = a(c.target);
                            return !b.searchOnEnter || 13 !== c.which || d.hasClass("add-group") || d.hasClass("add-rule") || d.hasClass("delete-group") || d.hasClass("delete-rule") || d.hasClass("fm-button") && d.is("[id$=_query]") ? b.closeOnEscape && 27 === c.which ? (a("#" + a.jgrid.jqID(i.modalhead)).find(".ui-jqdialog-titlebar-close").click(), !1) : void
                            0 : (a("#" + f + "_search").click(), !1)
                        }), u && a("#" + f + "_query").on("click", function () {
                            return a(".queryresult", m).toggle(), !1
                        }), void
                        0 === b.stringResult && (b.stringResult = b.multipleSearch), a("#" + f + "_search").on("click", function () {
                            var
                            c, g, j = {};
                            if (e = a("#" + f), e.find(".input-elm:focus").change(), y && b.multipleSearch ? (d.p_savedFilter = {}, g = a.jgrid.filterRefactor({
                                ruleGroup: a.extend(!0, {}, e.jqFilter("filterData")),
                                ssfield: z,
                                splitSelect: b.splitSelect,
                                groupOpSelect: b.groupOpSelect
                            }), d.p_savedFilter = a.extend(!0, {}, e.jqFilter("filterData"))) : g = e.jqFilter("filterData"), b.errorcheck && (e[0].hideError(), b.showQuery || e.jqFilter("toSQLString"), e[0].p.error)) return e[0].showError(), !1;
                            if (b.stringResult) {
                                try {
                                    c = JSON.stringify(g)
                                } catch (a) {}
                                "string" == typeof
                                c && (j[b.sFilter] = c, a.each([b.sField, b.sValue, b.sOper], function () {
                                    j[this] = ""
                                }))
                            } else b.multipleSearch ? (j[b.sFilter] = g, a.each([b.sField, b.sValue, b.sOper], function () {
                                j[this] = ""
                            })) : (j[b.sField] = g.rules[0].field, j[b.sValue] = g.rules[0].data, j[b.sOper] = g.rules[0].op, j[b.sFilter] = "");
                            return d.p.search = !0, a.extend(d.p.postData, j), h = a(d).triggerHandler("jqGridFilterSearch"), void
                            0 === h && (h = !0), h && a.isFunction(b.onSearch) && (h = b.onSearch.call(d, d.p.filters)), !1 !== h && a(d).trigger("reloadGrid", [{
                                page: 1
                            }]), b.closeAfterSearch && a.jgrid.hideModal("#" + a.jgrid.jqID(i.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(d.p.id),
                                jqm: b.jqModal,
                                onClose: b.onClose
                            }), !1
                        }), a("#" + f + "_reset").on("click", function () {
                            var
                            c = {}, e = a("#" + f);
                            return d.p.search = !1, d.p.resetsearch = !0, !1 === b.multipleSearch ? c[b.sField] = c[b.sValue] = c[b.sOper] = "" : c[b.sFilter] = "", e[0].resetFilter(), w && a(".ui-template", m).val("default"), a.extend(d.p.postData, c), h = a(d).triggerHandler("jqGridFilterReset"), void
                            0 === h && (h = !0), h && a.isFunction(b.onReset) && (h = b.onReset.call(d)), !1 !== h && a(d).trigger("reloadGrid", [{
                                page: 1
                            }]), b.closeAfterReset && a.jgrid.hideModal("#" + a.jgrid.jqID(i.themodal), {
                                gb: "#gbox_" + a.jgrid.jqID(d.p.id),
                                jqm: b.jqModal,
                                onClose: b.onClose
                            }), !1
                        }), c(a("#" + f)), a(".fm-button:not(." + l.disabled + ")", m).hover(function () {
                            a(this).addClass(l.hover)
                        }, function () {
                            a(this).removeClass(l.hover)
                        })
                    }
                }
            })
        },
        filterInput: function (b, c) {
            return c = a.extend(!0, {
                defaultSearch: "cn",
                groupOp: "OR",
                searchAll: !1,
                beforeSearch: null,
                afterSearch: null
            }, c || {}), this.each(function () {
                var
                d = this;
                if (d.grid) {
                    var
                    e, f, g, h = '{"groupOp":"' + c.groupOp + '","rules":[',
                        i = 0;
                    if (b += "", "local" === d.p.datatype) {
                        a.each(d.p.colModel, function () {
                            e = this.index || this.name, f = this.searchoptions || {}, g = c.defaultSearch ? c.defaultSearch : f.sopt ? f.sopt[0] : c.defaultSearch, this.search = !1 !== this.search, (this.search || c.searchAll) && (i > 0 && (h += ","), h += '{"field":"' + e + '",', h += '"op":"' + g + '",', h += '"data":"' + b.replace(/\\/g, "\\\\").replace(/\"/g, '\\"') + '"}', i++)
                        }), h += "]}", a.extend(d.p.postData, {
                            filters: h
                        }), a.each(["searchField", "searchString", "searchOper"], function (a, b) {
                            d.p.postData.hasOwnProperty(b) && delete
                            d.p.postData[b]
                        });
                        var
                        j = "stop" === a(d).triggerHandler("jqGridFilterInputBeforeSearch");
                        !j && a.isFunction(c.beforeSearch) && (j = c.beforeSearch.call(d)), j || a(d).jqGrid("setGridParam", {
                            search: !0
                        }).trigger("reloadGrid", [{
                            page: 1
                        }]), a(d).triggerHandler("jqGridFilterInputAfterSearch"), a.isFunction(c.afterSearch) && c.afterSearch.call(d)
                    }
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "./grid.common"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid.inlineEdit = a.jgrid.inlineEdit || {}, a.jgrid.extend({
        editRow: function (b, c, d, e, f, g, h, i, j) {
            var
            k = {}, l = a.makeArray(arguments).slice(1),
                m = this[0];
            return "object" === a.type(l[0]) ? k = l[0] : (void
            0 !== c && (k.keys = c), a.isFunction(d) && (k.oneditfunc = d), a.isFunction(e) && (k.successfunc = e), void
            0 !== f && (k.url = f), void
            0 !== g && (k.extraparam = g), a.isFunction(h) && (k.aftersavefunc = h), a.isFunction(i) && (k.errorfunc = i), a.isFunction(j) && (k.afterrestorefunc = j)), k = a.extend(!0, {
                keys: !1,
                keyevent: "keydown",
                oneditfunc: null,
                successfunc: null,
                url: null,
                extraparam: {},
                aftersavefunc: null,
                errorfunc: null,
                afterrestorefunc: null,
                restoreAfterError: !0,
                mtype: "POST",
                focusField: !0,
                saveui: "enable",
                savetext: a.jgrid.getRegional(m, "defaults.savetext")
            }, a.jgrid.inlineEdit, k), this.each(function () {
                var
                c, d, e, f, g, h, i = 0,
                    j = null,
                    l = {}, n = a(this).jqGrid("getStyleUI", m.p.styleUI + ".inlinedit", "inputClass", !0);
                if (m.grid && !1 !== (f = a(m).jqGrid("getInd", b, !0))) {
                    if (m.p.beforeAction = !0, h = a.isFunction(k.beforeEditRow) ? k.beforeEditRow.call(m, k, b) : void
                    0, void
                    0 === h && (h = !0), !h) return void(m.p.beforeAction = !1);
                    e = a(f).attr("editable") || "0", "0" !== e || a(f).hasClass("not-editable-row") || (g = m.p.colModel, a('td[role="gridcell"]', f).each(function (e) {
                        c = g[e].name;
                        var
                        f = !0 === m.p.treeGrid && c === m.p.ExpandColumn;
                        if (f) d = a("span:first", this).html();
                        else try {
                            d = a.unformat.call(m, this, {
                                rowId: b,
                                colModel: g[e]
                            }, e)
                        } catch (b) {
                            d = g[e].edittype && "textarea" === g[e].edittype ? a(this).text() : a(this).html()
                        }
                        if ("cb" !== c && "subgrid" !== c && "rn" !== c && (m.p.autoencode && (d = a.jgrid.htmlDecode(d)), l[c] = d, !0 === g[e].editable)) {
                            null === j && (j = e), f ? a("span:first", this).html("") : a(this).html("");
                            var
                            h = a.extend({}, g[e].editoptions || {}, {
                                id: b + "_" + c,
                                name: c,
                                rowId: b,
                                oper: "edit"
                            });
                            g[e].edittype || (g[e].edittype = "text"), ("&nbsp;" === d || "&#160;" === d || 1 === d.length && 160 === d.charCodeAt(0)) && (d = "");
                            var
                            k = a.jgrid.createEl.call(m, g[e].edittype, h, d, !0, a.extend({}, a.jgrid.ajaxOptions, m.p.ajaxSelectOptions || {}));
                            a(k).addClass("editable inline-edit-cell"), a.inArray(g[e].edittype, ["text", "textarea", "password", "select"]) > -1 && a(k).addClass(n), f ? a("span:first", this).append(k) : a(this).append(k), a.jgrid.bindEv.call(m, k, h), "select" === g[e].edittype && void
                            0 !== g[e].editoptions && !0 === g[e].editoptions.multiple && void
                            0 === g[e].editoptions.dataUrl && a.jgrid.msie() && a(k).width(a(k).width()), i++
                        }
                    }), i > 0 && (l.id = b, m.p.savedRow.push(l), a(f).attr("editable", "1"), k.focusField && ("number" == typeof
                    k.focusField && parseInt(k.focusField, 10) <= g.length && (j = k.focusField), setTimeout(function () {
                        var
                        b = a("td:eq(" + j + ") :input:visible", f).not(":disabled");
                        b.length > 0 && b.focus()
                    }, 0)), !0 === k.keys && a(f).on(k.keyevent, function (c) {
                        if (27 === c.keyCode) {
                            if (a(m).jqGrid("restoreRow", b, k), m.p.inlineNav) try {
                                a(m).jqGrid("showAddEditButtons")
                            } catch (a) {}
                            return !1
                        }
                        if (13 === c.keyCode) {
                            if ("TEXTAREA" === c.target.tagName) return !0;
                            if (a(m).jqGrid("saveRow", b, k) && m.p.inlineNav) try {
                                a(m).jqGrid("showAddEditButtons")
                            } catch (a) {}
                            return !1
                        }
                    }), a(m).triggerHandler("jqGridInlineEditRow", [b, k]), a.isFunction(k.oneditfunc) && k.oneditfunc.call(m, b)))
                }
            })
        },
        saveRow: function (b, c, d, e, f, g, h) {
            var
            i = a.makeArray(arguments).slice(1),
                j = {}, k = this[0];
            "object" === a.type(i[0]) ? j = i[0] : (a.isFunction(c) && (j.successfunc = c), void
            0 !== d && (j.url = d), void
            0 !== e && (j.extraparam = e), a.isFunction(f) && (j.aftersavefunc = f), a.isFunction(g) && (j.errorfunc = g), a.isFunction(h) && (j.afterrestorefunc = h)), j = a.extend(!0, {
                successfunc: null,
                url: null,
                extraparam: {},
                aftersavefunc: null,
                errorfunc: null,
                afterrestorefunc: null,
                restoreAfterError: !0,
                mtype: "POST",
                saveui: "enable",
                savetext: a.jgrid.getRegional(k, "defaults.savetext")
            }, a.jgrid.inlineEdit, j);
            var
            l, m, n, o, p, q = !1,
                r = {}, s = {}, t = {}, u = !1,
                v = a.trim(a(k).jqGrid("getStyleUI", k.p.styleUI + ".common", "error", !0));
            if (!k.grid) return q;
            if (!1 === (p = a(k).jqGrid("getInd", b, !0))) return q;
            var
            w = a.jgrid.getRegional(k, "errors"),
                x = a.jgrid.getRegional(k, "edit"),
                y = a.isFunction(j.beforeSaveRow) ? j.beforeSaveRow.call(k, j, b) : void
                0;
            if (void
            0 === y && (y = !0), y) {
                if (m = a(p).attr("editable"), j.url = j.url || k.p.editurl, "1" === m) {
                    var
                    z, A, B;
                    if (a('td[role="gridcell"]', p).each(function (b) {
                        if (z = k.p.colModel[b], l = z.name, B = "", "cb" !== l && "subgrid" !== l && !0 === z.editable && "rn" !== l && !a(this).hasClass("not-editable-cell")) {
                            switch (z.edittype) {
                                case "checkbox":
                                    var
                                    c = ["Yes", "No"];
                                    z.editoptions && z.editoptions.value && (c = z.editoptions.value.split(":")), r[l] = a("input", this).is(":checked") ? c[0] : c[1], B = a("input", this);
                                    break;
                                case "text":
                                case "password":
                                case "textarea":
                                case "button":
                                    r[l] = a("input, textarea", this).val(), B = a("input, textarea", this);
                                    break;
                                case "select":
                                    if (z.editoptions.multiple) {
                                        var
                                        d = a("select", this),
                                            e = [];
                                        r[l] = a(d).val(), r[l] ? r[l] = r[l].join(",") : r[l] = "", a("select option:selected", this).each(function (b, c) {
                                            e[b] = a(c).text()
                                        }), s[l] = e.join(",")
                                    } else r[l] = a("select option:selected", this).val(), s[l] = a("select option:selected", this).text();
                                    z.formatter && "select" === z.formatter && (s = {}), B = a("select", this);
                                    break;
                                case "custom":
                                    try {
                                        if (!z.editoptions || !a.isFunction(z.editoptions.custom_value)) throw "e1";
                                        if (r[l] = z.editoptions.custom_value.call(k, a(".customelement", this), "get"), void
                                        0 === r[l]) throw "e2"
                                    } catch (b) {
                                        "e1" === b ? a.jgrid.info_dialog(w.errcap, "function 'custom_value' " + x.msg.nodefined, x.bClose, {
                                            styleUI: k.p.styleUI
                                        }) : a.jgrid.info_dialog(w.errcap, b.message, x.bClose, {
                                            styleUI: k.p.styleUI
                                        })
                                    }
                            }
                            if (o = a.jgrid.checkValues.call(k, r[l], b), !1 === o[0]) return A = b, !1;
                            k.p.autoencode && (r[l] = a.jgrid.htmlEncode(r[l])), "clientArray" !== j.url && z.editoptions && !0 === z.editoptions.NullIfEmpty && "" === r[l] && (t[l] = "null", u = !0)
                        }
                    }), !1 === o[0]) {
                        try {
                            if (a.isFunction(k.p.validationCell)) k.p.validationCell.call(k, B, o[1], p.rowIndex, A);
                            else {
                                var
                                C = a(k).jqGrid("getGridRowById", b),
                                    D = a.jgrid.findPos(C);
                                a.jgrid.info_dialog(w.errcap, o[1], x.bClose, {
                                    left: D[0],
                                    top: D[1] + a(C).outerHeight(),
                                    styleUI: k.p.styleUI,
                                    onClose: function () {
                                        A >= 0 && a("#" + b + "_" + k.p.colModel[A].name).focus()
                                    }
                                })
                            }
                        } catch (a) {
                            alert(o[1])
                        }
                        return q
                    }
                    var
                    E, F = k.p.prmNames,
                        G = b;
                    if (E = !1 === k.p.keyName ? F.id : k.p.keyName, r) {
                        if (r[F.oper] = F.editoper, void
                        0 === r[E] || "" === r[E]) r[E] = b;
                        else if (p.id !== k.p.idPrefix + r[E]) {
                            var
                            H = a.jgrid.stripPref(k.p.idPrefix, b);
                            if (void
                            0 !== k.p._index[H] && (k.p._index[r[E]] = k.p._index[H], delete
                            k.p._index[H]), b = k.p.idPrefix + r[E], a(p).attr("id", b), k.p.selrow === G && (k.p.selrow = b), a.isArray(k.p.selarrrow)) {
                                var
                                I = a.inArray(G, k.p.selarrrow);
                                I >= 0 && (k.p.selarrrow[I] = b)
                            }
                            if (k.p.multiselect) {
                                var
                                J = "jqg_" + k.p.id + "_" + b;
                                a("input.cbox", p).attr("id", J).attr("name", J)
                            }
                        }
                        void
                        0 === k.p.inlineData && (k.p.inlineData = {}), r = a.extend({}, r, k.p.inlineData, j.extraparam)
                    }
                    if ("clientArray" === j.url) {
                        r = a.extend({}, r, s), k.p.autoencode && a.each(r, function (b, c) {
                            r[b] = a.jgrid.htmlDecode(c)
                        });
                        var
                        K, L = a(k).jqGrid("setRowData", b, r);
                        for (a(p).attr("editable", "0"), K = 0; K < k.p.savedRow.length; K++) if (String(k.p.savedRow[K].id) === String(G)) {
                            n = K;
                            break
                        }
                        n >= 0 && k.p.savedRow.splice(n, 1), a(k).triggerHandler("jqGridInlineAfterSaveRow", [b, L, r, j]), a.isFunction(j.aftersavefunc) && j.aftersavefunc.call(k, b, L, r, j), q = !0, a(p).removeClass("jqgrid-new-row").off("keydown")
                    } else a(k).jqGrid("progressBar", {
                        method: "show",
                        loadtype: j.saveui,
                        htmlcontent: j.savetext
                    }), t = a.extend({}, r, t), t[E] = a.jgrid.stripPref(k.p.idPrefix, t[E]), a.ajax(a.extend({
                        url: j.url,
                        data: a.isFunction(k.p.serializeRowData) ? k.p.serializeRowData.call(k, t) : t,
                        type: j.mtype,
                        async: !1,
                        complete: function (c, d) {
                            if (a(k).jqGrid("progressBar", {
                                method: "hide",
                                loadtype: j.saveui,
                                htmlcontent: j.savetext
                            }), "success" === d) {
                                var
                                e, f, g = !0;
                                if (e = a(k).triggerHandler("jqGridInlineSuccessSaveRow", [c, b, j]), a.isArray(e) || (e = [!0, t]), e[0] && a.isFunction(j.successfunc) && (e = j.successfunc.call(k, c)), a.isArray(e) ? (g = e[0], r = e[1] || r) : g = e, !0 === g) {
                                    for (k.p.autoencode && a.each(r, function (b, c) {
                                        r[b] = a.jgrid.htmlDecode(c)
                                    }), u && a.each(r, function (a) {
                                        "null" === r[a] && (r[a] = "")
                                    }), r = a.extend({}, r, s), a(k).jqGrid("setRowData", b, r), a(p).attr("editable", "0"), f = 0; f < k.p.savedRow.length; f++) if (String(k.p.savedRow[f].id) === String(b)) {
                                        n = f;
                                        break
                                    }
                                    n >= 0 && k.p.savedRow.splice(n, 1), a(k).triggerHandler("jqGridInlineAfterSaveRow", [b, c, r, j]), a.isFunction(j.aftersavefunc) && j.aftersavefunc.call(k, b, c, r, j), q = !0, a(p).removeClass("jqgrid-new-row").off("keydown")
                                } else a(k).triggerHandler("jqGridInlineErrorSaveRow", [b, c, d, null, j]), a.isFunction(j.errorfunc) && j.errorfunc.call(k, b, c, d, null), !0 === j.restoreAfterError && a(k).jqGrid("restoreRow", b, j)
                            }
                        },
                        error: function (c, d, e) {
                            if (a("#lui_" + a.jgrid.jqID(k.p.id)).hide(), a(k).triggerHandler("jqGridInlineErrorSaveRow", [b, c, d, e, j]), a.isFunction(j.errorfunc)) j.errorfunc.call(k, b, c, d, e);
                            else {
                                var
                                f = c.responseText || c.statusText;
                                try {
                                    a.jgrid.info_dialog(w.errcap, '<div class="' + v + '">' + f + "</div>", x.bClose, {
                                        buttonalign: "right",
                                        styleUI: k.p.styleUI
                                    })
                                } catch (a) {
                                    alert(f)
                                }
                            }!0 === j.restoreAfterError && a(k).jqGrid("restoreRow", b, j)
                        }
                    }, a.jgrid.ajaxOptions, k.p.ajaxRowOptions || {}))
                }
                return q
            }
        },
        restoreRow: function (b, c) {
            var
            d = a.makeArray(arguments).slice(1),
                e = {};
            return "object" === a.type(d[0]) ? e = d[0] : a.isFunction(c) && (e.afterrestorefunc = c), e = a.extend(!0, {}, a.jgrid.inlineEdit, e), this.each(function () {
                var
                c, d, f = this,
                    g = -1,
                    h = {};
                if (f.grid && !1 !== (c = a(f).jqGrid("getInd", b, !0))) {
                    var
                    i = a.isFunction(e.beforeCancelRow) ? e.beforeCancelRow.call(f, e, b) : void
                    0;
                    if (void
                    0 === i && (i = !0), i) {
                        for (d = 0; d < f.p.savedRow.length; d++) if (String(f.p.savedRow[d].id) === String(b)) {
                            g = d;
                            break
                        }
                        if (g >= 0) {
                            if (a.isFunction(a.fn.datepicker)) try {
                                a("input.hasDatepicker", "#" + a.jgrid.jqID(c.id)).datepicker("hide")
                            } catch (a) {}
                            a.each(f.p.colModel, function () {
                                f.p.savedRow[g].hasOwnProperty(this.name) && (h[this.name] = f.p.savedRow[g][this.name])
                            }), a(f).jqGrid("setRowData", b, h), a(c).attr("editable", "0").off("keydown"), f.p.savedRow.splice(g, 1), a("#" + a.jgrid.jqID(b), "#" + a.jgrid.jqID(f.p.id)).hasClass("jqgrid-new-row") && setTimeout(function () {
                                a(f).jqGrid("delRowData", b), a(f).jqGrid("showAddEditButtons")
                            }, 0)
                        }
                        a(f).triggerHandler("jqGridInlineAfterRestoreRow", [b]), a.isFunction(e.afterrestorefunc) && e.afterrestorefunc.call(f, b)
                    }
                }
            })
        },
        addRow: function (b) {
            return b = a.extend(!0, {
                rowID: null,
                initdata: {},
                position: "first",
                useDefValues: !0,
                useFormatter: !1,
                addRowParams: {
                    extraparam: {}
                }
            }, b || {}), this.each(function () {
                if (this.grid) {
                    var
                    c = this;
                    c.p.beforeAction = !0;
                    var
                    d = a.isFunction(b.beforeAddRow) ? b.beforeAddRow.call(c, b.addRowParams) : void
                    0;
                    if (void
                    0 === d && (d = !0), !d) return void(c.p.beforeAction = !1);
                    if (b.rowID = a.isFunction(b.rowID) ? b.rowID.call(c, b) : null != b.rowID ? b.rowID : a.jgrid.randId(), !0 === b.useDefValues && a(c.p.colModel).each(function () {
                        if (this.editoptions && this.editoptions.defaultValue) {
                            var
                            d = this.editoptions.defaultValue,
                                e = a.isFunction(d) ? d.call(c) : d;
                            b.initdata[this.name] = e
                        }
                    }), a(c).jqGrid("addRowData", b.rowID, b.initdata, b.position), b.rowID = c.p.idPrefix + b.rowID, a("#" + a.jgrid.jqID(b.rowID), "#" + a.jgrid.jqID(c.p.id)).addClass("jqgrid-new-row"), b.useFormatter) a("#" + a.jgrid.jqID(b.rowID) + " .ui-inline-edit", "#" + a.jgrid.jqID(c.p.id)).click();
                    else {
                        var
                        e = c.p.prmNames,
                            f = e.oper;
                        b.addRowParams.extraparam[f] = e.addoper, a(c).jqGrid("editRow", b.rowID, b.addRowParams), a(c).jqGrid("setSelection", b.rowID)
                    }
                }
            })
        },
        inlineNav: function (b, c) {
            var
            d = this[0],
                e = a.jgrid.getRegional(d, "nav"),
                f = a.jgrid.styleUI[d.p.styleUI].inlinedit;
            return c = a.extend(!0, {
                edit: !0,
                editicon: f.icon_edit_nav,
                add: !0,
                addicon: f.icon_add_nav,
                save: !0,
                saveicon: f.icon_save_nav,
                cancel: !0,
                cancelicon: f.icon_cancel_nav,
                addParams: {
                    addRowParams: {
                        extraparam: {}
                    }
                },
                editParams: {},
                restoreAfterSelect: !0,
                saveAfterSelect: !1
            }, e, c || {}), this.each(function () {
                if (this.grid && !this.p.inlineNav) {
                    var
                    f = a.jgrid.jqID(d.p.id),
                        g = a.trim(a(d).jqGrid("getStyleUI", d.p.styleUI + ".common", "disabled", !0));
                    if (d.p.navGrid || a(d).jqGrid("navGrid", b, {
                        refresh: !1,
                        edit: !1,
                        add: !1,
                        del: !1,
                        search: !1,
                        view: !1
                    }), a(d).data("inlineNav") || a(d).data("inlineNav", c), d.p.force_regional && (c = a.extend(c, e)), d.p.inlineNav = !0, !0 === c.addParams.useFormatter) {
                        var
                        h, i = d.p.colModel;
                        for (h = 0; h < i.length; h++) if (i[h].formatter && "actions" === i[h].formatter) {
                            if (i[h].formatoptions) {
                                var
                                j = {
                                    keys: !1,
                                    onEdit: null,
                                    onSuccess: null,
                                    afterSave: null,
                                    onError: null,
                                    afterRestore: null,
                                    extraparam: {},
                                    url: null
                                }, k = a.extend(j, i[h].formatoptions);
                                c.addParams.addRowParams = {
                                    keys: k.keys,
                                    oneditfunc: k.onEdit,
                                    successfunc: k.onSuccess,
                                    url: k.url,
                                    extraparam: k.extraparam,
                                    aftersavefunc: k.afterSave,
                                    errorfunc: k.onError,
                                    afterrestorefunc: k.afterRestore
                                }
                            }
                            break
                        }
                    }
                    c.add && a(d).jqGrid("navButtonAdd", b, {
                        caption: c.addtext,
                        title: c.addtitle,
                        buttonicon: c.addicon,
                        id: d.p.id + "_iladd",
                        internal: !0,
                        onClickButton: function () {
                            void
                            0 === d.p.beforeAction && (d.p.beforeAction = !0), a(d).jqGrid("addRow", c.addParams), !c.addParams.useFormatter && d.p.beforeAction && (a("#" + f + "_ilsave").removeClass(g), a("#" + f + "_ilcancel").removeClass(g), a("#" + f + "_iladd").addClass(g), a("#" + f + "_iledit").addClass(g))
                        }
                    }), c.edit && a(d).jqGrid("navButtonAdd", b, {
                        caption: c.edittext,
                        title: c.edittitle,
                        buttonicon: c.editicon,
                        id: d.p.id + "_iledit",
                        internal: !0,
                        onClickButton: function () {
                            var
                            b = a(d).jqGrid("getGridParam", "selrow");
                            b ? (void
                            0 === d.p.beforeAction && (d.p.beforeAction = !0), a(d).jqGrid("editRow", b, c.editParams), d.p.beforeAction && (a("#" + f + "_ilsave").removeClass(g), a("#" + f + "_ilcancel").removeClass(g), a("#" + f + "_iladd").addClass(g), a("#" + f + "_iledit").addClass(g))) : (a.jgrid.viewModal("#alertmod_" + f, {
                                gbox: "#gbox_" + f,
                                jqm: !0
                            }), a("#jqg_alrt").focus())
                        }
                    }), c.save && (a(d).jqGrid("navButtonAdd", b, {
                        caption: c.savetext || "",
                        title: c.savetitle || "Save row",
                        buttonicon: c.saveicon,
                        id: d.p.id + "_ilsave",
                        internal: !0,
                        onClickButton: function () {
                            var
                            b = d.p.savedRow[0].id;
                            if (b) {
                                var
                                e = d.p.prmNames,
                                    g = e.oper,
                                    h = c.editParams;
                                a("#" + a.jgrid.jqID(b), "#" + f).hasClass("jqgrid-new-row") ? (c.addParams.addRowParams.extraparam[g] = e.addoper, h = c.addParams.addRowParams) : (c.editParams.extraparam || (c.editParams.extraparam = {}), c.editParams.extraparam[g] = e.editoper), a(d).jqGrid("saveRow", b, h) && a(d).jqGrid("showAddEditButtons")
                            } else a.jgrid.viewModal("#alertmod_" + f, {
                                gbox: "#gbox_" + f,
                                jqm: !0
                            }), a("#jqg_alrt").focus()
                        }
                    }), a("#" + f + "_ilsave").addClass(g)), c.cancel && (a(d).jqGrid("navButtonAdd", b, {
                        caption: c.canceltext || "",
                        title: c.canceltitle || "Cancel row editing",
                        buttonicon: c.cancelicon,
                        id: d.p.id + "_ilcancel",
                        internal: !0,
                        onClickButton: function () {
                            var
                            b = d.p.savedRow[0].id,
                                e = c.editParams;
                            b ? (a("#" + a.jgrid.jqID(b), "#" + f).hasClass("jqgrid-new-row") && (e = c.addParams.addRowParams), a(d).jqGrid("restoreRow", b, e), a(d).jqGrid("showAddEditButtons")) : (a.jgrid.viewModal("#alertmod", {
                                gbox: "#gbox_" + f,
                                jqm: !0
                            }), a("#jqg_alrt").focus())
                        }
                    }), a("#" + f + "_ilcancel").addClass(g)), !0 !== c.restoreAfterSelect && !0 !== c.saveAfterSelect || a(d).on("jqGridBeforeSelectRow.inlineNav", function (b, e) {
                        d.p.savedRow.length > 0 && !0 === d.p.inlineNav && e !== d.p.selrow && null !== d.p.selrow && (d.p.selrow === c.addParams.rowID ? a(d).jqGrid("delRowData", d.p.selrow) : !0 === c.restoreAfterSelect ? a(d).jqGrid("restoreRow", d.p.selrow, c.editParams) : a(d).jqGrid("saveRow", d.p.selrow, c.editParams), a(d).jqGrid("showAddEditButtons"))
                    })
                }
            })
        },
        showAddEditButtons: function () {
            return this.each(function () {
                if (this.grid) {
                    var
                    b = a.jgrid.jqID(this.p.id),
                        c = a.trim(a(this).jqGrid("getStyleUI", this.p.styleUI + ".common", "disabled", !0));
                    a("#" + b + "_ilsave").addClass(c), a("#" + b + "_ilcancel").addClass(c), a("#" + b + "_iladd").removeClass(c), a("#" + b + "_iledit").removeClass(c)
                }
            })
        },
        showSaveCancelButtons: function () {
            return this.each(function () {
                if (this.grid) {
                    var
                    b = a.jgrid.jqID(this.p.id),
                        c = a.trim(a(this).jqGrid("getStyleUI", this.p.styleUI + ".common", "disabled", !0));
                    a("#" + b + "_ilsave").removeClass(c), a("#" + b + "_ilcancel").removeClass(c), a("#" + b + "_iladd").addClass(c), a("#" + b + "_iledit").addClass(c)
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid.extend({
        editCell: function (b, c, d) {
            return this.each(function () {
                var
                e, f, g, h, i = this,
                    j = a(this).jqGrid("getStyleUI", i.p.styleUI + ".common", "highlight", !0),
                    k = a(this).jqGrid("getStyleUI", i.p.styleUI + ".common", "hover", !0),
                    l = a(this).jqGrid("getStyleUI", i.p.styleUI + ".celledit", "inputClass", !0);
                if (i.grid && !0 === i.p.cellEdit) {
                    if (c = parseInt(c, 10), i.p.selrow = i.rows[b].id, i.p.knv || a(i).jqGrid("GridNav"), i.p.savedRow.length > 0) {
                        if (!0 === d && b == i.p.iRow && c == i.p.iCol) return;
                        a(i).jqGrid("saveCell", i.p.savedRow[0].id, i.p.savedRow[0].ic)
                    } else window.setTimeout(function () {
                        a("#" + a.jgrid.jqID(i.p.knv)).attr("tabindex", "-1").focus()
                    }, 1);
                    if (h = i.p.colModel[c], "subgrid" !== (e = h.name) && "cb" !== e && "rn" !== e) {
                        try {
                            g = a(i.rows[b].cells[c])
                        } catch (d) {
                            g = a("td:eq(" + c + ")", i.rows[b])
                        }
                        if (!0 !== h.editable || !0 !== d || g.hasClass("not-editable-cell") || a.isFunction(i.p.isCellEditable) && !i.p.isCellEditable.call(i, e, b, c)) parseInt(i.p.iCol, 10) >= 0 && parseInt(i.p.iRow, 10) >= 0 && a(i.rows[i.p.iRow]).removeClass("selected-row " + k).find("td:eq(" + i.p.iCol + ")").removeClass("edit-cell " + j), g.addClass("edit-cell " + j), a(i.rows[b]).addClass("selected-row " + k), f = g.html().replace(/\&#160\;/gi, ""), a(i).triggerHandler("jqGridSelectCell", [i.rows[b].id, e, f, b, c]), a.isFunction(i.p.onSelectCell) && i.p.onSelectCell.call(i, i.rows[b].id, e, f, b, c);
                        else {
                            parseInt(i.p.iCol, 10) >= 0 && parseInt(i.p.iRow, 10) >= 0 && a(i.rows[i.p.iRow]).removeClass("selected-row " + k).find("td:eq(" + i.p.iCol + ")").removeClass("edit-cell " + j), g.addClass("edit-cell " + j), a(i.rows[b]).addClass("selected-row " + k);
                            try {
                                f = a.unformat.call(i, g, {
                                    rowId: i.rows[b].id,
                                    colModel: h
                                }, c)
                            } catch (a) {
                                f = h.edittype && "textarea" === h.edittype ? g.text() : g.html()
                            }
                            if (i.p.autoencode && (f = a.jgrid.htmlDecode(f)), h.edittype || (h.edittype = "text"), i.p.savedRow.push({
                                id: b,
                                ic: c,
                                name: e,
                                v: f
                            }), ("&nbsp;" === f || "&#160;" === f || 1 === f.length && 160 === f.charCodeAt(0)) && (f = ""), a.isFunction(i.p.formatCell)) {
                                var
                                m = i.p.formatCell.call(i, i.rows[b].id, e, f, b, c);
                                void
                                0 !== m && (f = m)
                            }
                            a(i).triggerHandler("jqGridBeforeEditCell", [i.rows[b].id, e, f, b, c]), a.isFunction(i.p.beforeEditCell) && i.p.beforeEditCell.call(i, i.rows[b].id, e, f, b, c);
                            var
                            n = a.extend({}, h.editoptions || {}, {
                                id: b + "_" + e,
                                name: e,
                                rowId: i.rows[b].id,
                                oper: "edit"
                            }),
                                o = a.jgrid.createEl.call(i, h.edittype, n, f, !0, a.extend({}, a.jgrid.ajaxOptions, i.p.ajaxSelectOptions || {}));
                            a.inArray(h.edittype, ["text", "textarea", "password", "select"]) > -1 && a(o).addClass(l), g.html("").append(o).attr("tabindex", "0"), a.jgrid.bindEv.call(i, o, n), window.setTimeout(function () {
                                a(o).focus()
                            }, 1), a("input, select, textarea", g).on("keydown", function (d) {
                                if (27 === d.keyCode && (a("input.hasDatepicker", g).length > 0 ? a(".ui-datepicker").is(":hidden") ? a(i).jqGrid("restoreCell", b, c) : a("input.hasDatepicker", g).datepicker("hide") : a(i).jqGrid("restoreCell", b, c)), 13 === d.keyCode && !d.shiftKey) return a(i).jqGrid("saveCell", b, c), !1;
                                if (9 === d.keyCode) {
                                    if (i.grid.hDiv.loading) return !1;
                                    d.shiftKey ? a(i).jqGrid("prevCell", b, c) : a(i).jqGrid("nextCell", b, c)
                                }
                                d.stopPropagation()
                            }), a(i).triggerHandler("jqGridAfterEditCell", [i.rows[b].id, e, f, b, c]), a.isFunction(i.p.afterEditCell) && i.p.afterEditCell.call(i, i.rows[b].id, e, f, b, c)
                        }
                        i.p.iCol = c, i.p.iRow = b
                    }
                }
            })
        },
        saveCell: function (b, c) {
            return this.each(function () {
                var
                d, e = this,
                    f = a.jgrid.getRegional(this, "errors"),
                    g = a.jgrid.getRegional(this, "edit");
                if (e.grid && !0 === e.p.cellEdit) {
                    if (null !== (d = e.p.savedRow.length >= 1 ? 0 : null)) {
                        var
                        h, i, j = a("td:eq(" + c + ")", e.rows[b]),
                            k = e.p.colModel[c],
                            l = k.name,
                            m = a.jgrid.jqID(l),
                            n = a(j).offset();
                        switch (k.edittype) {
                            case "select":
                                if (k.editoptions.multiple) {
                                    var
                                    o = a("#" + b + "_" + m, e.rows[b]),
                                        p = [];
                                    h = a(o).val(), h ? h.join(",") : h = "", a("option:selected", o).each(function (b, c) {
                                        p[b] = a(c).text()
                                    }), i = p.join(",")
                                } else h = a("#" + b + "_" + m + " option:selected", e.rows[b]).val(), i = a("#" + b + "_" + m + " option:selected", e.rows[b]).text();
                                k.formatter && (i = h);
                                break;
                            case "checkbox":
                                var
                                q = ["Yes", "No"];
                                k.editoptions && k.editoptions.value && (q = k.editoptions.value.split(":")), h = a("#" + b + "_" + m, e.rows[b]).is(":checked") ? q[0] : q[1], i = h;
                                break;
                            case "password":
                            case "text":
                            case "textarea":
                            case "button":
                                h = a("#" + b + "_" + m, e.rows[b]).val(), i = h;
                                break;
                            case "custom":
                                try {
                                    if (!k.editoptions || !a.isFunction(k.editoptions.custom_value)) throw "e1";
                                    if (void
                                    0 === (h = k.editoptions.custom_value.call(e, a(".customelement", j), "get"))) throw "e2";
                                    i = h
                                } catch (b) {
                                    "e1" === b ? a.jgrid.info_dialog(f.errcap, "function 'custom_value' " + g.msg.nodefined, g.bClose, {
                                        styleUI: e.p.styleUI
                                    }) : "e2" === b ? a.jgrid.info_dialog(f.errcap, "function 'custom_value' " + g.msg.novalue, g.bClose, {
                                        styleUI: e.p.styleUI
                                    }) : a.jgrid.info_dialog(f.errcap, b.message, g.bClose, {
                                        styleUI: e.p.styleUI
                                    })
                                }
                        }
                        if (i !== e.p.savedRow[d].v) {
                            var
                            r = a(e).triggerHandler("jqGridBeforeSaveCell", [e.rows[b].id, l, h, b, c]);
                            if (r && (h = r, i = r), a.isFunction(e.p.beforeSaveCell)) {
                                var
                                s = e.p.beforeSaveCell.call(e, e.rows[b].id, l, h, b, c);
                                s && (h = s, i = s)
                            }
                            var
                            t = a.jgrid.checkValues.call(e, h, c),
                                u = !1;
                            if (!0 === t[0]) {
                                var
                                v = a(e).triggerHandler("jqGridBeforeSubmitCell", [e.rows[b].id, l, h, b, c]) || {};
                                a.isFunction(e.p.beforeSubmitCell) && ((v = e.p.beforeSubmitCell.call(e, e.rows[b].id, l, h, b, c)) || (v = {}));
                                var
                                w = a(e).triggerHandler("jqGridOnSubmitCell", [e.rows[b].id, l, h, b, c]);
                                if (void
                                0 === w && (w = !0), a.isFunction(e.p.onSubmitCell) && void
                                0 === (w = e.p.onSubmitCell(e.rows[b].id, l, h, b, c)) && (w = !0), !1 === w) return;
                                if (a("input.hasDatepicker", j).length > 0 && a("input.hasDatepicker", j).datepicker("hide"), "remote" === e.p.cellsubmit) if (e.p.cellurl) {
                                    var
                                    x = {};
                                    e.p.autoencode && (h = a.jgrid.htmlEncode(h)), k.editoptions && k.editoptions.NullIfEmpty && "" === h && (h = "null", u = !0), x[l] = h;
                                    var
                                    y, z, A;
                                    A = e.p.prmNames, y = A.id, z = A.oper, x[y] = a.jgrid.stripPref(e.p.idPrefix, e.rows[b].id), x[z] = A.editoper, x = a.extend(v, x), a(e).jqGrid("progressBar", {
                                        method: "show",
                                        loadtype: e.p.loadui,
                                        htmlcontent: a.jgrid.getRegional(e, "defaults.savetext")
                                    }), e.grid.hDiv.loading = !0, a.ajax(a.extend({
                                        url: e.p.cellurl,
                                        data: a.isFunction(e.p.serializeCellData) ? e.p.serializeCellData.call(e, x, l) : x,
                                        type: "POST",
                                        complete: function (d, k) {
                                            if (a(e).jqGrid("progressBar", {
                                                method: "hide",
                                                loadtype: e.p.loadui
                                            }), e.grid.hDiv.loading = !1, "success" === k) {
                                                var
                                                o = a(e).triggerHandler("jqGridAfterSubmitCell", [e, d, x.id, l, h, b, c]) || [!0, ""];
                                                !0 === o[0] && a.isFunction(e.p.afterSubmitCell) && (o = e.p.afterSubmitCell.call(e, d, x.id, l, h, b, c)), !0 === o[0] ? (u && (h = ""), a(j).empty(), a(e).jqGrid("setCell", e.rows[b].id, c, i, !1, !1, !0), a(j).addClass("dirty-cell"), a(e.rows[b]).addClass("edited"), a(e).triggerHandler("jqGridAfterSaveCell", [e.rows[b].id, l, h, b, c]), a.isFunction(e.p.afterSaveCell) && e.p.afterSaveCell.call(e, e.rows[b].id, l, h, b, c), e.p.savedRow.splice(0, 1)) : (a(e).triggerHandler("jqGridErrorCell", [d, k]), a.isFunction(e.p.errorCell) ? e.p.errorCell.call(e, d, k) : a.jgrid.info_dialog(f.errcap, o[1], g.bClose, {
                                                    styleUI: e.p.styleUI,
                                                    top: n.top + 30,
                                                    left: n.left,
                                                    onClose: function () {
                                                        e.p.restoreCellonFail || a("#" + b + "_" + m, e.rows[b]).focus()
                                                    }
                                                }), e.p.restoreCellonFail && a(e).jqGrid("restoreCell", b, c))
                                            }
                                        },
                                        error: function (d, h, i) {
                                            a("#lui_" + a.jgrid.jqID(e.p.id)).hide(), e.grid.hDiv.loading = !1, a(e).triggerHandler("jqGridErrorCell", [d, h, i]), a.isFunction(e.p.errorCell) ? e.p.errorCell.call(e, d, h, i) : a.jgrid.info_dialog(f.errcap, d.status + " : " + d.statusText + "<br/>" + h, g.bClose, {
                                                styleUI: e.p.styleUI,
                                                top: n.top + 30,
                                                left: n.left,
                                                onClose: function () {
                                                    e.p.restoreCellonFail || a("#" + b + "_" + m, e.rows[b]).focus()
                                                }
                                            }), e.p.restoreCellonFail && a(e).jqGrid("restoreCell", b, c)
                                        }
                                    }, a.jgrid.ajaxOptions, e.p.ajaxCellOptions || {}))
                                } else try {
                                    a.jgrid.info_dialog(f.errcap, f.nourl, g.bClose, {
                                        styleUI: e.p.styleUI
                                    }), e.p.restoreCellonFail && a(e).jqGrid("restoreCell", b, c)
                                } catch (a) {}
                                "clientArray" === e.p.cellsubmit && (a(j).empty(), a(e).jqGrid("setCell", e.rows[b].id, c, i, !1, !1, !0), a(j).addClass("dirty-cell"), a(e.rows[b]).addClass("edited"), a(e).triggerHandler("jqGridAfterSaveCell", [e.rows[b].id, l, h, b, c]), a.isFunction(e.p.afterSaveCell) && e.p.afterSaveCell.call(e, e.rows[b].id, l, h, b, c), e.p.savedRow.splice(0, 1))
                            } else try {
                                a.isFunction(e.p.validationCell) ? e.p.validationCell.call(e, a("#" + b + "_" + m, e.rows[b]), t[1], b, c) : (window.setTimeout(function () {
                                    a.jgrid.info_dialog(f.errcap, h + " " + t[1], g.bClose, {
                                        styleUI: e.p.styleUI,
                                        top: n.top + 30,
                                        left: n.left,
                                        onClose: function () {
                                            e.p.restoreCellonFail || a("#" + b + "_" + m, e.rows[b]).focus()
                                        }
                                    })
                                }, 50), e.p.restoreCellonFail && a(e).jqGrid("restoreCell", b, c))
                            } catch (a) {
                                alert(t[1])
                            }
                        } else a(e).jqGrid("restoreCell", b, c)
                    }
                    window.setTimeout(function () {
                        a("#" + a.jgrid.jqID(e.p.knv)).attr("tabindex", "-1").focus()
                    }, 0)
                }
            })
        },
        restoreCell: function (b, c) {
            return this.each(function () {
                var
                d, e = this;
                if (e.grid && !0 === e.p.cellEdit) {
                    if (null !== (d = e.p.savedRow.length >= 1 ? 0 : null)) {
                        var
                        f = a("td:eq(" + c + ")", e.rows[b]);
                        if (a.isFunction(a.fn.datepicker)) try {
                            a("input.hasDatepicker", f).datepicker("hide")
                        } catch (a) {}
                        a(f).empty().attr("tabindex", "-1"), a(e).jqGrid("setCell", e.rows[b].id, c, e.p.savedRow[d].v, !1, !1, !0), a(e).triggerHandler("jqGridAfterRestoreCell", [e.rows[b].id, e.p.savedRow[d].v, b, c]), a.isFunction(e.p.afterRestoreCell) && e.p.afterRestoreCell.call(e, e.rows[b].id, e.p.savedRow[d].v, b, c), e.p.savedRow.splice(0, 1)
                    }
                    window.setTimeout(function () {
                        a("#" + e.p.knv).attr("tabindex", "-1").focus()
                    }, 0)
                }
            })
        },
        nextCell: function (b, c) {
            return this.each(function () {
                var
                d, e = this,
                    f = !1;
                if (e.grid && !0 === e.p.cellEdit) {
                    for (d = c + 1; d < e.p.colModel.length; d++) if (!0 === e.p.colModel[d].editable && (!a.isFunction(e.p.isCellEditable) || e.p.isCellEditable.call(e, e.p.colModel[d].name, b, d))) {
                        f = d;
                        break
                    }!1 !== f ? a(e).jqGrid("editCell", b, f, !0) : e.p.savedRow.length > 0 && a(e).jqGrid("saveCell", b, c)
                }
            })
        },
        prevCell: function (b, c) {
            return this.each(function () {
                var
                d, e = this,
                    f = !1;
                if (e.grid && !0 === e.p.cellEdit) {
                    for (d = c - 1; d >= 0; d--) if (!0 === e.p.colModel[d].editable && (!a.isFunction(e.p.isCellEditable) || e.p.isCellEditable.call(e, e.p.colModel[d].name, b, d))) {
                        f = d;
                        break
                    }!1 !== f ? a(e).jqGrid("editCell", b, f, !0) : e.p.savedRow.length > 0 && a(e).jqGrid("saveCell", b, c)
                }
            })
        },
        GridNav: function () {
            return this.each(function () {
                function
                b(b, c, e) {
                    if ("v" === e.substr(0, 1)) {
                        var
                        f = a(d.grid.bDiv)[0].clientHeight,
                            g = a(d.grid.bDiv)[0].scrollTop,
                            h = d.rows[b].offsetTop + d.rows[b].clientHeight,
                            i = d.rows[b].offsetTop;
                        "vd" === e && h >= f && (a(d.grid.bDiv)[0].scrollTop = a(d.grid.bDiv)[0].scrollTop + d.rows[b].clientHeight), "vu" === e && i < g && (a(d.grid.bDiv)[0].scrollTop = a(d.grid.bDiv)[0].scrollTop - d.rows[b].clientHeight)
                    }
                    if ("h" === e) {
                        var
                        j = a(d.grid.bDiv)[0].clientWidth,
                            k = a(d.grid.bDiv)[0].scrollLeft,
                            l = d.rows[b].cells[c].offsetLeft + d.rows[b].cells[c].clientWidth,
                            m = d.rows[b].cells[c].offsetLeft;
                        l >= j + parseInt(k, 10) ? a(d.grid.bDiv)[0].scrollLeft = a(d.grid.bDiv)[0].scrollLeft + d.rows[b].cells[c].clientWidth : m < k && (a(d.grid.bDiv)[0].scrollLeft = a(d.grid.bDiv)[0].scrollLeft - d.rows[b].cells[c].clientWidth)
                    }
                }

                function
                c(a, b) {
                    var
                    c, e;
                    if ("lft" === b) for (c = a + 1, e = a; e >= 0; e--) if (!0 !== d.p.colModel[e].hidden) {
                        c = e;
                        break
                    }
                    if ("rgt" === b) for (c = a - 1, e = a; e < d.p.colModel.length; e++) if (!0 !== d.p.colModel[e].hidden) {
                        c = e;
                        break
                    }
                    return c
                }
                var
                d = this;
                if (d.grid && !0 === d.p.cellEdit) {
                    d.p.knv = d.p.id + "_kn";
                    var
                    e, f, g = a("<div style='position:fixed;top:0px;width:1px;height:1px;' tabindex='0'><div tabindex='-1' style='width:1px;height:1px;' id='" + d.p.knv + "'></div></div>");
                    a(g).insertBefore(d.grid.cDiv), a("#" + d.p.knv).focus().keydown(function (g) {
                        switch (f = g.keyCode, "rtl" === d.p.direction && (37 === f ? f = 39 : 39 === f && (f = 37)), f) {
                            case
                            38:
                                d.p.iRow - 1 > 0 && (b(d.p.iRow - 1, d.p.iCol, "vu"), a(d).jqGrid("editCell", d.p.iRow - 1, d.p.iCol, !1));
                                break;
                            case
                            40:
                                d.p.iRow + 1 <= d.rows.length - 1 && (b(d.p.iRow + 1, d.p.iCol, "vd"), a(d).jqGrid("editCell", d.p.iRow + 1, d.p.iCol, !1));
                                break;
                            case
                            37:
                                d.p.iCol - 1 >= 0 && (e = c(d.p.iCol - 1, "lft"), b(d.p.iRow, e, "h"), a(d).jqGrid("editCell", d.p.iRow, e, !1));
                                break;
                            case
                            39:
                                d.p.iCol + 1 <= d.p.colModel.length - 1 && (e = c(d.p.iCol + 1, "rgt"), b(d.p.iRow, e, "h"), a(d).jqGrid("editCell", d.p.iRow, e, !1));
                                break;
                            case
                            13:
                                parseInt(d.p.iCol, 10) >= 0 && parseInt(d.p.iRow, 10) >= 0 && a(d).jqGrid("editCell", d.p.iRow, d.p.iCol, !0);
                                break;
                            default:
                                return !0
                        }
                        return !1
                    })
                }
            })
        },
        getChangedCells: function (b) {
            var
            c = [];
            return b || (b = "all"), this.each(function () {
                var
                d, e = this;
                e.grid && !0 === e.p.cellEdit && a(e.rows).each(function (f) {
                    var
                    g = {};
                    a(this).hasClass("edited") && (a("td", this).each(function (c) {
                        if ("cb" !== (d = e.p.colModel[c].name) && "subgrid" !== d) if ("dirty" === b) {
                            if (a(this).hasClass("dirty-cell")) try {
                                g[d] = a.unformat.call(e, this, {
                                    rowId: e.rows[f].id,
                                    colModel: e.p.colModel[c]
                                }, c)
                            } catch (b) {
                                g[d] = a.jgrid.htmlDecode(a(this).html())
                            }
                        } else try {
                            g[d] = a.unformat.call(e, this, {
                                rowId: e.rows[f].id,
                                colModel: e.p.colModel[c]
                            }, c)
                        } catch (b) {
                            g[d] = a.jgrid.htmlDecode(a(this).html())
                        }
                    }), g.id = this.id, c.push(g))
                })
            }), c
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.fn.jqm = function (d) {
        var
        f = {
            overlay: 50,
            closeoverlay: !0,
            overlayClass: "jqmOverlay",
            closeClass: "jqmClose",
            trigger: ".jqModal",
            ajax: e,
            ajaxText: "",
            target: e,
            modal: e,
            toTop: e,
            onShow: e,
            onHide: e,
            onLoad: e
        };
        return this.each(function () {
            if (this._jqm) return c[this._jqm].c = a.extend({}, c[this._jqm].c, d);
            b++, this._jqm = b, c[b] = {
                c: a.extend(f, a.jqm.params, d),
                a: e,
                w: a(this).addClass("jqmID" + b),
                s: b
            }, f.trigger && a(this).jqmAddTrigger(f.trigger)
        })
    }, a.fn.jqmAddClose = function (a) {
        return j(this, a, "jqmHide")
    }, a.fn.jqmAddTrigger = function (a) {
        return j(this, a, "jqmShow")
    }, a.fn.jqmShow = function (b) {
        return this.each(function () {
            a.jqm.open(this._jqm, b)
        })
    }, a.fn.jqmHide = function (b) {
        return this.each(function () {
            a.jqm.close(this._jqm, b)
        })
    }, a.jqm = {
        hash: {},
        open: function (b, g) {
            var
            i = c[b],
                j = i.c,
                k = "." + j.closeClass,
                l = parseInt(i.w.css("z-index"));
            l = l > 0 ? l : 3e3;
            var
            m = a("<div></div>").css({
                height: "100%",
                width: "100%",
                position: "fixed",
                left: 0,
                top: 0,
                "z-index": l - 1,
                opacity: j.overlay / 100
            });
            if (i.a) return e;
            if (i.t = g, i.a = !0, i.w.css("z-index", l), j.modal ? (d[0] || setTimeout(function () {
                new
                h("bind")
            }, 1), d.push(b)) : j.overlay > 0 ? j.closeoverlay && i.w.jqmAddClose(m) : m = e, i.o = m ? m.addClass(j.overlayClass).prependTo("body") : e, j.ajax) {
                var
                n = j.target || i.w,
                    o = j.ajax;
                n = "string" == typeof
                n ? a(n, i.w) : a(n), o = "@" === o.substr(0, 1) ? a(g).attr(o.substring(1)) : o, n.html(j.ajaxText).load(o, function () {
                    j.onLoad && j.onLoad.call(this, i), k && i.w.jqmAddClose(a(k, i.w)), f(i)
                })
            } else k && i.w.jqmAddClose(a(k, i.w));
            return j.toTop && i.o && i.w.before('<span id="jqmP' + i.w[0]._jqm + '"></span>').insertAfter(i.o), j.onShow ? j.onShow(i) : i.w.show(), f(i), e
        },
        close: function (b) {
            var
            f = c[b];
            return f.a ? (f.a = e, d[0] && (d.pop(), d[0] || new
            h("unbind")), f.c.toTop && f.o && a("#jqmP" + f.w[0]._jqm).after(f.w).remove(), f.c.onHide ? f.c.onHide(f) : (f.w.hide(), f.o && f.o.remove()), e) : e
        },
        params: {}
    };
    var
    b = 0,
        c = a.jqm.hash,
        d = [],
        e = !1,
        f = function (a) {
            void
            0 === a.c.focusField && (a.c.focusField = 0), a.c.focusField >= 0 && g(a)
        }, g = function (b) {
            try {
                a(":input:visible", b.w)[parseInt(b.c.focusField, 10)].focus()
            } catch (a) {}
        }, h = function (b) {
            a(document)[b]("keypress", i)[b]("keydown", i)[b]("mousedown", i)
        }, i = function (b) {
            var
            e = c[d[d.length - 1]],
                f = !a(b.target).parents(".jqmID" + e.s)[0];
            return f && (a(".jqmID" + e.s).each(function () {
                var
                c = a(this),
                    d = c.offset();
                if (d.top <= b.pageY && b.pageY <= d.top + c.height() && d.left <= b.pageX && b.pageX <= d.left + c.width()) return f = !1, !1
            }), g(e)), !f
        }, j = function (b, d, f) {
            return b.each(function () {
                var
                b = this._jqm;
                a(d).each(function () {
                    this[f] || (this[f] = [], a(this).click(function () {
                        for (var
                        a in {
                            jqmShow: 1,
                            jqmHide: 1
                        }) for (var
                        b in this[a]) c[this[a][b]] && c[this[a][b]].w[a](this);
                        return e
                    })), this[f].push(b)
                })
            })
        }
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.fn.jqDrag = function (a) {
        return g(this, a, "d")
    }, a.fn.jqResize = function (a, b) {
        return g(this, a, "r", b)
    }, a.jqDnR = {
        dnr: {},
        e: 0,
        drag: function (a) {
            return "d" == e.k ? f.css({
                left: e.X + a.pageX - e.pX,
                top: e.Y + a.pageY - e.pY
            }) : (f.css({
                width: Math.max(a.pageX - e.pX + e.W, 0),
                height: Math.max(a.pageY - e.pY + e.H, 0)
            }), c && b.css({
                width: Math.max(a.pageX - c.pX + c.W, 0),
                height: Math.max(a.pageY - c.pY + c.H, 0)
            })), !1
        },
        stop: function () {
            a(document).off("mousemove", d.drag).off("mouseup", d.stop)
        }
    };
    var
    b, c, d = a.jqDnR,
        e = d.dnr,
        f = d.e,
        g = function (d, g, j, k) {
            return d.each(function () {
                g = g ? a(g, d) : d, g.on("mousedown", {
                    e: d,
                    k: j
                }, function (d) {
                    var
                    g = d.data,
                        j = {};
                    if (f = g.e, b = !! k && a(k), "relative" != f.css("position")) try {
                        f.position(j)
                    } catch (a) {}
                    if (e = {
                        X: j.left || h("left") || 0,
                        Y: j.top || h("top") || 0,
                        W: h("width") || f[0].scrollWidth || 0,
                        H: h("height") || f[0].scrollHeight || 0,
                        pX: d.pageX,
                        pY: d.pageY,
                        k: g.k
                    }, c = !(!b || "d" == g.k) && {
                        X: j.left || i("left") || 0,
                        Y: j.top || i("top") || 0,
                        W: b[0].offsetWidth || i("width") || 0,
                        H: b[0].offsetHeight || i("height") || 0,
                        pX: d.pageX,
                        pY: d.pageY,
                        k: g.k
                    }, a("input.hasDatepicker", f[0])[0]) try {
                        a("input.hasDatepicker", f[0]).datepicker("hide")
                    } catch (a) {}
                    return a(document).mousemove(a.jqDnR.drag).mouseup(a.jqDnR.stop), !1
                })
            })
        }, h = function (a) {
            return parseInt(f.css(a), 10) || !1
        }, i = function (a) {
            return parseInt(b.css(a), 10) || !1
        };
    a.fn.tinyDraggable = function (b) {
        var
        c = a.extend({
            handle: 0,
            exclude: 0
        }, b);
        return this.each(function () {
            var
            b, d, e = a(this);
            (c.handle ? a(c.handle, e) : e).on({
                mousedown: function (f) {
                    if (!c.exclude || !~a.inArray(f.target, a(c.exclude, e))) {
                        f.preventDefault();
                        var
                        g = e.offset();
                        b = f.pageX - g.left, d = f.pageY - g.top, a(document).on("mousemove.drag", function (a) {
                            e.offset({
                                top: a.pageY - d,
                                left: a.pageX - b
                            })
                        })
                    }
                },
                mouseup: function (b) {
                    a(document).off("mousemove.drag")
                }
            })
        })
    }
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid.extend({
        setSubGrid: function () {
            return this.each(function () {
                var
                b, c, d = this,
                    e = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].subgrid,
                    f = {
                        plusicon: e.icon_plus,
                        minusicon: e.icon_minus,
                        openicon: e.icon_open,
                        expandOnLoad: !1,
                        selectOnExpand: !1,
                        selectOnCollapse: !1,
                        reloadOnExpand: !0
                    };
                if (d.p.subGridOptions = a.extend(f, d.p.subGridOptions || {}), d.p.colNames.unshift(""), d.p.colModel.unshift({
                    name: "subgrid",
                    width: a.jgrid.cell_width ? d.p.subGridWidth + d.p.cellLayout : d.p.subGridWidth,
                    sortable: !1,
                    resizable: !1,
                    hidedlg: !0,
                    search: !1,
                    fixed: !0
                }), b = d.p.subGridModel, b[0]) for (b[0].align = a.extend([], b[0].align || []), c = 0; c < b[0].name.length; c++) b[0].align[c] = b[0].align[c] || "left"
            })
        },
        addSubGridCell: function (b, c) {
            var
            d, e, f, g = "";
            return this.each(function () {
                g = this.formatCol(b, c), e = this.p.id, d = this.p.subGridOptions.plusicon, f = a.jgrid.styleUI[this.p.styleUI || "jQueryUI"].common
            }), '<td role="gridcell" aria-describedby="' + e + '_subgrid" class="ui-sgcollapsed sgcollapsed" ' + g + "><a style='cursor:pointer;' class='ui-sghref'><span class='" + f.icon_base + " " + d + "'></span></a></td>"
        },
        addSubGrid: function (b, c) {
            return this.each(function () {
                var
                d = this;
                if (d.grid) {
                    var
                    e, f, g, h, i, j = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].base,
                        k = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].common,
                        l = function (b, c, e) {
                            var
                            f = a("<td align='" + d.p.subGridModel[0].align[e] + "'></td>").html(c);
                            a(b).append(f)
                        }, m = function (b, c) {
                            var
                            e, f, g, h = a("<table class='" + j.rowTable + " ui-common-table'><tbody></tbody></table>"),
                                i = a("<tr></tr>");
                            for (f = 0; f < d.p.subGridModel[0].name.length; f++) e = a("<th class='" + j.headerBox + " ui-th-subgrid ui-th-column ui-th-" + d.p.direction + "'></th>"), a(e).html(d.p.subGridModel[0].name[f]), a(e).width(d.p.subGridModel[0].width[f]), a(i).append(e);
                            a(h).append(i), b && (g = d.p.xmlReader.subgrid, a(g.root + " " + g.row, b).each(function () {
                                if (i = a("<tr class='" + k.content + " ui-subtblcell'></tr>"), !0 === g.repeatitems) a(g.cell, this).each(function (b) {
                                    l(i, a(this).text() || "&#160;", b)
                                });
                                else {
                                    var
                                    b = d.p.subGridModel[0].mapping || d.p.subGridModel[0].name;
                                    if (b) for (f = 0; f < b.length; f++) l(i, a(b[f], this).text() || "&#160;", f)
                                }
                                a(h).append(i)
                            }));
                            var
                            m = a("table:first", d.grid.bDiv).attr("id") + "_";
                            return a("#" + a.jgrid.jqID(m + c)).append(h), d.grid.hDiv.loading = !1, a("#load_" + a.jgrid.jqID(d.p.id)).hide(), !1
                        }, n = function (b, c) {
                            var
                            e, f, g, h, i, m, n = a("<table class='" + j.rowTable + " ui-common-table'><tbody></tbody></table>"),
                                o = a("<tr></tr>");
                            for (g = 0; g < d.p.subGridModel[0].name.length; g++) e = a("<th class='" + j.headerBox + " ui-th-subgrid ui-th-column ui-th-" + d.p.direction + "'></th>"), a(e).html(d.p.subGridModel[0].name[g]), a(e).width(d.p.subGridModel[0].width[g]), a(o).append(e);
                            if (a(n).append(o), b && (i = d.p.jsonReader.subgrid, void
                            0 !== (f = a.jgrid.getAccessor(b, i.root)))) for (g = 0; g < f.length; g++) {
                                if (h = f[g], o = a("<tr class='" + k.content + " ui-subtblcell'></tr>"), !0 === i.repeatitems) for (i.cell && (h = h[i.cell]), m = 0; m < h.length; m++) l(o, h[m] || "&#160;", m);
                                else {
                                    var
                                    p = d.p.subGridModel[0].mapping || d.p.subGridModel[0].name;
                                    if (p.length) for (m = 0; m < p.length; m++) l(o, h[p[m]] || "&#160;", m)
                                }
                                a(n).append(o)
                            }
                            var
                            q = a("table:first", d.grid.bDiv).attr("id") + "_";
                            return a("#" + a.jgrid.jqID(q + c)).append(n), d.grid.hDiv.loading = !1, a("#load_" + a.jgrid.jqID(d.p.id)).hide(), !1
                        }, o = function (b) {
                            var
                            c, e, f, g;
                            if (c = a(b).attr("id"), e = {
                                nd_: (new
                                Date).getTime()
                            }, e[d.p.prmNames.subgridid] = c, !d.p.subGridModel[0]) return !1;
                            if (d.p.subGridModel[0].params) for (g = 0; g < d.p.subGridModel[0].params.length; g++) for (f = 0; f < d.p.colModel.length; f++) d.p.colModel[f].name === d.p.subGridModel[0].params[g] && (e[d.p.colModel[f].name] = a("td:eq(" + f + ")", b).text().replace(/\&#160\;/gi, ""));
                            if (!d.grid.hDiv.loading) switch (d.grid.hDiv.loading = !0, a("#load_" + a.jgrid.jqID(d.p.id)).show(), d.p.subgridtype || (d.p.subgridtype = d.p.datatype), a.isFunction(d.p.subgridtype) ? d.p.subgridtype.call(d, e) : d.p.subgridtype = d.p.subgridtype.toLowerCase(), d.p.subgridtype) {
                                case "xml":
                                case "json":
                                    a.ajax(a.extend({
                                        type: d.p.mtype,
                                        url: a.isFunction(d.p.subGridUrl) ? d.p.subGridUrl.call(d, e) : d.p.subGridUrl,
                                        dataType: d.p.subgridtype,
                                        data: a.isFunction(d.p.serializeSubGridData) ? d.p.serializeSubGridData.call(d, e) : e,
                                        complete: function (b) {
                                            "xml" === d.p.subgridtype ? m(b.responseXML, c) : n(a.jgrid.parse(b.responseText), c), b = null
                                        }
                                    }, a.jgrid.ajaxOptions, d.p.ajaxSubgridOptions || {}))
                            }
                            return !1
                        }, p = 0;
                    a.each(d.p.colModel, function () {
                        !0 !== this.hidden && "rn" !== this.name && "cb" !== this.name || p++
                    });
                    var
                    q, r = d.rows.length,
                        s = 1,
                        t = a.isFunction(d.p.isHasSubGrid);
                    for (void
                    0 !== c && c > 0 && (s = c, r = c + 1); s < r;) a(d.rows[s]).hasClass("jqgrow") && (d.p.scroll && a(d.rows[s].cells[b]).off("click"), q = null, t && (q = d.p.isHasSubGrid.call(d, d.rows[s].id)), !1 === q ? d.rows[s].cells[b].innerHTML = "" : a(d.rows[s].cells[b]).on("click", function () {
                        var
                        c = a(this).parent("tr")[0];
                        if (f = d.p.id, e = c.id, i = a("#" + f + "_" + e + "_expandedContent"), a(this).hasClass("sgcollapsed")) {
                            if (h = a(d).triggerHandler("jqGridSubGridBeforeExpand", [f + "_" + e, e]), h = !1 !== h && "stop" !== h, h && a.isFunction(d.p.subGridBeforeExpand) && (h = d.p.subGridBeforeExpand.call(d, f + "_" + e, e)), !1 === h) return !1;
                            !0 === d.p.subGridOptions.reloadOnExpand || !1 === d.p.subGridOptions.reloadOnExpand && !i.hasClass("ui-subgrid") ? (g = b >= 1 ? "<td colspan='" + b + "'>&#160;</td>" : "", a(c).after("<tr role='row' id='" + f + "_" + e + "_expandedContent' class='ui-subgrid ui-sg-expanded'>" + g + "<td class='" + k.content + " subgrid-cell'><span class='" + k.icon_base + " " + d.p.subGridOptions.openicon + "'></span></td><td colspan='" + parseInt(d.p.colNames.length - 1 - p, 10) + "' class='" + k.content + " subgrid-data'><div id=" + f + "_" + e + " class='tablediv'></div></td></tr>"), a(d).triggerHandler("jqGridSubGridRowExpanded", [f + "_" + e, e]), a.isFunction(d.p.subGridRowExpanded) ? d.p.subGridRowExpanded.call(d, f + "_" + e, e) : o(c)) : i.show().removeClass("ui-sg-collapsed").addClass("ui-sg-expanded"), a(this).html("<a style='cursor:pointer;' class='ui-sghref'><span class='" + k.icon_base + " " + d.p.subGridOptions.minusicon + "'></span></a>").removeClass("sgcollapsed").addClass("sgexpanded"), d.p.subGridOptions.selectOnExpand && a(d).jqGrid("setSelection", e)
                        } else if (a(this).hasClass("sgexpanded")) {
                            if (h = a(d).triggerHandler("jqGridSubGridRowColapsed", [f + "_" + e, e]), h = !1 !== h && "stop" !== h, h && a.isFunction(d.p.subGridRowColapsed) && (h = d.p.subGridRowColapsed.call(d, f + "_" + e, e)), !1 === h) return !1;
                            !0 === d.p.subGridOptions.reloadOnExpand ? i.remove(".ui-subgrid") : i.hasClass("ui-subgrid") && i.hide().addClass("ui-sg-collapsed").removeClass("ui-sg-expanded"), a(this).html("<a style='cursor:pointer;' class='ui-sghref'><span class='" + k.icon_base + " " + d.p.subGridOptions.plusicon + "'></span></a>").removeClass("sgexpanded").addClass("sgcollapsed"), d.p.subGridOptions.selectOnCollapse && a(d).jqGrid("setSelection", e)
                        }
                        return !1
                    })), s++;
                    !0 === d.p.subGridOptions.expandOnLoad && a(d.rows).filter(".jqgrow").each(function (b, c) {
                        a(c.cells[0]).click()
                    }), d.subGridXml = function (a, b) {
                        m(a, b)
                    }, d.subGridJson = function (a, b) {
                        n(a, b)
                    }
                }
            })
        },
        expandSubGridRow: function (b) {
            return this.each(function () {
                var
                c = this;
                if ((c.grid || b) && !0 === c.p.subGrid) {
                    var
                    d = a(this).jqGrid("getInd", b, !0);
                    if (d) {
                        var
                        e = a("td.sgcollapsed", d)[0];
                        e && a(e).trigger("click")
                    }
                }
            })
        },
        collapseSubGridRow: function (b) {
            return this.each(function () {
                var
                c = this;
                if ((c.grid || b) && !0 === c.p.subGrid) {
                    var
                    d = a(this).jqGrid("getInd", b, !0);
                    if (d) {
                        var
                        e = a("td.sgexpanded", d)[0];
                        e && a(e).trigger("click")
                    }
                }
            })
        },
        toggleSubGridRow: function (b) {
            return this.each(function () {
                var
                c = this;
                if ((c.grid || b) && !0 === c.p.subGrid) {
                    var
                    d = a(this).jqGrid("getInd", b, !0);
                    if (d) {
                        var
                        e = a("td.sgcollapsed", d)[0];
                        e ? a(e).trigger("click") : (e = a("td.sgexpanded", d)[0]) && a(e).trigger("click")
                    }
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid.extend({
        groupingSetup: function () {
            return this.each(function () {
                var
                b, c, d, e = this,
                    f = e.p.colModel,
                    g = e.p.groupingView,
                    h = a.jgrid.styleUI[e.p.styleUI || "jQueryUI"].grouping;
                if (null === g || "object" != typeof
                g && !a.isFunction(g)) e.p.grouping = !1;
                else if (g.plusicon || (g.plusicon = h.icon_plus), g.minusicon || (g.minusicon = h.icon_minus), g.groupField.length) {
                    for (void
                    0 === g.visibiltyOnNextGrouping && (g.visibiltyOnNextGrouping = []), g.lastvalues = [], g._locgr || (g.groups = []), g.counters = [], b = 0; b < g.groupField.length; b++) g.groupOrder[b] || (g.groupOrder[b] = "asc"), g.groupText[b] || (g.groupText[b] = "{0}"), "boolean" != typeof
                    g.groupColumnShow[b] && (g.groupColumnShow[b] = !0), "boolean" != typeof
                    g.groupSummary[b] && (g.groupSummary[b] = !1), g.groupSummaryPos[b] || (g.groupSummaryPos[b] = "footer"), !0 === g.groupColumnShow[b] ? (g.visibiltyOnNextGrouping[b] = !0, a(e).jqGrid("showCol", g.groupField[b])) : (g.visibiltyOnNextGrouping[b] = a("#" + a.jgrid.jqID(e.p.id + "_" + g.groupField[b])).is(":visible"), a(e).jqGrid("hideCol", g.groupField[b]));
                    for (g.summary = [], g.hideFirstGroupCol && a.isArray(g.formatDisplayField) && !a.isFunction(g.formatDisplayField[0]) && (g.formatDisplayField[0] = function (a) {
                        return a
                    }), c = 0, d = f.length; c < d; c++) g.hideFirstGroupCol && (f[c].hidden || g.groupField[0] !== f[c].name || (f[c].formatter = function () {
                        return ""
                    })), f[c].summaryType && (f[c].summaryDivider ? g.summary.push({
                        nm: f[c].name,
                        st: f[c].summaryType,
                        v: "",
                        sd: f[c].summaryDivider,
                        vd: "",
                        sr: f[c].summaryRound,
                        srt: f[c].summaryRoundType || "round"
                    }) : g.summary.push({
                        nm: f[c].name,
                        st: f[c].summaryType,
                        v: "",
                        sr: f[c].summaryRound,
                        srt: f[c].summaryRoundType || "round"
                    }))
                } else e.p.grouping = !1
            })
        },
        groupingPrepare: function (b, c) {
            return this.each(function () {
                var
                d, e, f, g, h, i = this.p.groupingView,
                    j = this,
                    k = function () {
                        a.isFunction(this.st) ? this.v = this.st.call(j, this.v, this.nm, b) : (this.v = a(j).jqGrid("groupingCalculations.handler", this.st, this.v, this.nm, this.sr, this.srt, b), "avg" === this.st.toLowerCase() && this.sd && (this.vd = a(j).jqGrid("groupingCalculations.handler", this.st, this.vd, this.sd, this.sr, this.srt, b)))
                    }, l = i.groupField.length,
                    m = 0;
                for (d = 0; d < l; d++) e = i.groupField[d], g = i.displayField[d], f = b[e], h = null == g ? null : b[g], null == h && (h = f), void
                0 !== f && (0 === c ? (i.groups.push({
                    idx: d,
                    dataIndex: e,
                    value: f,
                    displayValue: h,
                    startRow: c,
                    cnt: 1,
                    summary: []
                }), i.lastvalues[d] = f, i.counters[d] = {
                    cnt: 1,
                    pos: i.groups.length - 1,
                    summary: a.extend(!0, [], i.summary)
                }, a.each(i.counters[d].summary, k), i.groups[i.counters[d].pos].summary = i.counters[d].summary) : "object" == typeof
                f || (a.isArray(i.isInTheSameGroup) && a.isFunction(i.isInTheSameGroup[d]) ? i.isInTheSameGroup[d].call(j, i.lastvalues[d], f, d, i) : i.lastvalues[d] === f) ? 1 === m ? (i.groups.push({
                    idx: d,
                    dataIndex: e,
                    value: f,
                    displayValue: h,
                    startRow: c,
                    cnt: 1,
                    summary: []
                }), i.lastvalues[d] = f, i.counters[d] = {
                    cnt: 1,
                    pos: i.groups.length - 1,
                    summary: a.extend(!0, [], i.summary)
                }, a.each(i.counters[d].summary, k), i.groups[i.counters[d].pos].summary = i.counters[d].summary) : (i.counters[d].cnt += 1, i.groups[i.counters[d].pos].cnt = i.counters[d].cnt, a.each(i.counters[d].summary, k), i.groups[i.counters[d].pos].summary = i.counters[d].summary) : (i.groups.push({
                    idx: d,
                    dataIndex: e,
                    value: f,
                    displayValue: h,
                    startRow: c,
                    cnt: 1,
                    summary: []
                }), i.lastvalues[d] = f, m = 1, i.counters[d] = {
                    cnt: 1,
                    pos: i.groups.length - 1,
                    summary: a.extend(!0, [], i.summary)
                }, a.each(i.counters[d].summary, k), i.groups[i.counters[d].pos].summary = i.counters[d].summary))
            }), this
        },
        groupingToggle: function (b) {
            return this.each(function () {
                var
                c = this,
                    d = c.p.groupingView,
                    e = b.split("_"),
                    f = parseInt(e[e.length - 2], 10);
                e.splice(e.length - 2, 2);
                var
                g, h, i = e.join("_"),
                    j = d.minusicon,
                    k = d.plusicon,
                    l = a("#" + a.jgrid.jqID(b)),
                    m = l.length ? l[0].nextSibling : null,
                    n = a("#" + a.jgrid.jqID(b) + " span.tree-wrap-" + c.p.direction),
                    o = function (b) {
                        var
                        c = a.map(b.split(" "), function (a) {
                            if (a.substring(0, i.length + 1) === i + "_") return parseInt(a.substring(i.length + 1), 10)
                        });
                        return c.length > 0 ? c[0] : void
                        0
                    }, p = !1,
                    q = !1,
                    r = !! c.p.frozenColumns && c.p.id + "_frozen",
                    s = !! r && a("#" + a.jgrid.jqID(b), "#" + a.jgrid.jqID(r)),
                    t = s && s.length ? s[0].nextSibling : null;
                if (n.hasClass(j)) {
                    if (m) for (; m && !(void
                    0 !== (g = o(m.className)) && g <= f);) a(m).hide(), m = m.nextSibling, r && (a(t).hide(), t = t.nextSibling);
                    n.removeClass(j).addClass(k), p = !0
                } else {
                    if (m) for (h = void
                    0; m;) {
                        if (g = o(m.className), void
                        0 === h && (h = void
                        0 === g), q = a(m).hasClass("ui-subgrid") && a(m).hasClass("ui-sg-collapsed"), void
                        0 !== g) {
                            if (g <= f) break;
                            g === f + 1 && (q || (a(m).show().find(">td>span.tree-wrap-" + c.p.direction).removeClass(j).addClass(k), r && a(t).show().find(">td>span.tree-wrap-" + c.p.direction).removeClass(j).addClass(k)))
                        } else h && (q || (a(m).show(), r && a(t).show()));
                        m = m.nextSibling, r && (t = t.nextSibling)
                    }
                    n.removeClass(k).addClass(j)
                }
                a(c).triggerHandler("jqGridGroupingClickGroup", [b, p]), a.isFunction(c.p.onClickGroup) && c.p.onClickGroup.call(c, b, p)
            }), !1
        },
        groupingRender: function (b, c, d, e) {
            return this.each(function () {
                function
                f(a, b, c) {
                    var
                    d, e = !1;
                    if (0 === b) e = c[a];
                    else {
                        var
                        f = c[a].idx;
                        if (0 === f) e = c[a];
                        else for (d = a; d >= 0; d--) if (c[d].idx === f - b) {
                            e = c[d];
                            break
                        }
                    }
                    return e
                }

                function
                g(b, d, e, g) {
                    var
                    h, i, j = f(b, d, e),
                        l = k.p.colModel,
                        m = j.cnt,
                        n = "";
                    for (i = g; i < c; i++) {
                        var
                        o = "<td " + k.formatCol(i, 1, "") + ">&#160;</td>",
                            p = "{0}";
                        a.each(j.summary, function () {
                            if (this.nm === l[i].name) {
                                l[i].summaryTpl && (p = l[i].summaryTpl), "string" == typeof
                                this.st && "avg" === this.st.toLowerCase() && (this.sd && this.vd ? this.v = this.v / this.vd : this.v && m > 0 && (this.v = this.v / m));
                                try {
                                    this.groupCount = j.cnt, this.groupIndex = j.dataIndex, this.groupValue = j.value, h = k.formatter("", this.v, i, this)
                                } catch (a) {
                                    h = this.v
                                }
                                return o = "<td " + k.formatCol(i, 1, "") + ">" + a.jgrid.template(p, h, j.cnt) + "</td>", !1
                            }
                        }), n += o
                    }
                    return n
                }
                var
                h, i, j, k = this,
                    l = k.p.groupingView,
                    m = "",
                    n = "",
                    o = l.groupCollapse ? l.plusicon : l.minusicon,
                    p = [],
                    q = l.groupField.length,
                    r = a.jgrid.styleUI[k.p.styleUI || "jQueryUI"].common;
                o = o + " tree-wrap-" + k.p.direction, a.each(k.p.colModel, function (a, b) {
                    var
                    c;
                    for (c = 0; c < q; c++) if (l.groupField[c] === b.name) {
                        p[c] = a;
                        break
                    }
                });
                var
                s, t = 0,
                    u = a.makeArray(l.groupSummary);
                u.reverse(), s = k.p.multiselect ? ' colspan="2"' : "", a.each(l.groups, function (f, v) {
                    if (l._locgr && !(v.startRow + v.cnt > (d - 1) * e && v.startRow < d * e)) return !0;
                    t++, i = k.p.id + "ghead_" + v.idx, h = i + "_" + f, n = "<span style='cursor:pointer;margin-right:8px;margin-left:5px;' class='" + r.icon_base + " " + o + "' onclick=\"jQuery('#" + a.jgrid.jqID(k.p.id) + "').jqGrid('groupingToggle','" + h + "');return false;\"></span>";
                    try {
                        j = a.isArray(l.formatDisplayField) && a.isFunction(l.formatDisplayField[v.idx]) ? l.formatDisplayField[v.idx].call(k, v.displayValue, v.value, k.p.colModel[p[v.idx]], v.idx, l) : k.formatter(h, v.displayValue, p[v.idx], v.value)
                    } catch (a) {
                        j = v.displayValue
                    }
                    var
                    w = "";
                    if (w = a.isFunction(l.groupText[v.idx]) ? l.groupText[v.idx].call(k, j, v.cnt, v.summary) : a.jgrid.template(l.groupText[v.idx], j, v.cnt, v.summary), "string" != typeof
                    w && "number" != typeof
                    w && (w = j), "header" === l.groupSummaryPos[v.idx] ? (m += '<tr id="' + h + '"' + (l.groupCollapse && v.idx > 0 ? ' style="display:none;" ' : " ") + 'role="row" class= "' + r.content + " jqgroup ui-row-" + k.p.direction + " " + i + '"><td style="padding-left:' + 12 * v.idx + 'px;"' + s + ">" + n + w + "</td>", m += g(f, 0, l.groups, !1 === l.groupColumnShow[v.idx] ? "" === s ? 2 : 3 : "" === s ? 1 : 2), m += "</tr>") : m += '<tr id="' + h + '"' + (l.groupCollapse && v.idx > 0 ? ' style="display:none;" ' : " ") + 'role="row" class= "' + r.content + " jqgroup ui-row-" + k.p.direction + " " + i + '"><td style="padding-left:' + 12 * v.idx + 'px;" colspan="' + (!1 === l.groupColumnShow[v.idx] ? c - 1 : c) + '">' + n + w + "</td></tr>", q - 1 === v.idx) {
                        var
                        x, y, z = l.groups[f + 1],
                            A = 0,
                            B = v.startRow,
                            C = void
                            0 !== z ? z.startRow : l.groups[f].startRow + l.groups[f].cnt;
                        for (l._locgr && (A = (d - 1) * e) > v.startRow && (B = A), x = B; x < C && b[x - A]; x++) m += b[x - A].join("");
                        if ("header" !== l.groupSummaryPos[v.idx]) {
                            var
                            D;
                            if (void
                            0 !== z) {
                                for (D = 0; D < l.groupField.length && z.dataIndex !== l.groupField[D]; D++);
                                t = l.groupField.length - D
                            }
                            for (y = 0; y < t; y++) if (u[y]) {
                                var
                                E = "";
                                l.groupCollapse && !l.showSummaryOnHide && (E = ' style="display:none;"'), m += "<tr" + E + ' jqfootlevel="' + (v.idx - y) + '" role="row" class="' + r.content + " jqfoot ui-row-" + k.p.direction + '">', m += g(f, y, l.groups, 0), m += "</tr>"
                            }
                            t = D
                        }
                    }
                }), a("#" + a.jgrid.jqID(k.p.id) + " tbody:first").append(m), m = null
            })
        },
        groupingGroupBy: function (b, c) {
            return this.each(function () {
                var
                d = this;
                "string" == typeof
                b && (b = [b]);
                var
                e = d.p.groupingView;
                d.p.grouping = !0, e._locgr = !1, void
                0 === e.visibiltyOnNextGrouping && (e.visibiltyOnNextGrouping = []);
                var
                f;
                for (f = 0; f < e.groupField.length; f++)!e.groupColumnShow[f] && e.visibiltyOnNextGrouping[f] && a(d).jqGrid("showCol", e.groupField[f]);
                for (f = 0; f < b.length; f++) e.visibiltyOnNextGrouping[f] = a("#" + a.jgrid.jqID(d.p.id) + "_" + a.jgrid.jqID(b[f])).is(":visible");
                d.p.groupingView = a.extend(d.p.groupingView, c || {}), e.groupField = b, a(d).trigger("reloadGrid")
            })
        },
        groupingRemove: function (b) {
            return this.each(function () {
                var
                c = this;
                if (void
                0 === b && (b = !0), c.p.grouping = !1, !0 === b) {
                    var
                    d, e = c.p.groupingView;
                    for (d = 0; d < e.groupField.length; d++)!e.groupColumnShow[d] && e.visibiltyOnNextGrouping[d] && a(c).jqGrid("showCol", e.groupField);
                    a("tr.jqgroup, tr.jqfoot", "#" + a.jgrid.jqID(c.p.id) + " tbody:first").remove(), a("tr.jqgrow:hidden", "#" + a.jgrid.jqID(c.p.id) + " tbody:first").show()
                } else a(c).trigger("reloadGrid")
            })
        },
        groupingCalculations: {
            handler: function (a, b, c, d, e, f) {
                var
                g = {
                    sum: function () {
                        return parseFloat(b || 0) + parseFloat(f[c] || 0)
                    },
                    min: function () {
                        return "" === b ? parseFloat(f[c] || 0) : Math.min(parseFloat(b), parseFloat(f[c] || 0))
                    },
                    max: function () {
                        return "" === b ? parseFloat(f[c] || 0) : Math.max(parseFloat(b), parseFloat(f[c] || 0))
                    },
                    count: function () {
                        return "" === b && (b = 0), f.hasOwnProperty(c) ? b + 1 : 0
                    },
                    avg: function () {
                        return g.sum()
                    }
                };
                if (!g[a]) throw "jqGrid Grouping No such method: " + a;
                var
                h = g[a]();
                if (null != d) if ("fixed" === e) h = h.toFixed(d);
                else {
                    var
                    i = Math.pow(10, d);
                    h = Math.round(h * i) / i
                }
                return h
            }
        },
        setGroupHeaders: function (b) {
            return b = a.extend({
                useColSpanStyle: !1,
                groupHeaders: []
            }, b || {}), this.each(function () {
                var
                c, d, e, f, g, h, i, j, k, l, m, n, o, p, q = this,
                    r = 0,
                    s = q.p.colModel,
                    t = s.length,
                    u = q.grid.headers,
                    v = a("table.ui-jqgrid-htable", q.grid.hDiv),
                    w = v.children("thead").children("tr.ui-jqgrid-labels:last").addClass("jqg-second-row-header"),
                    x = v.children("thead"),
                    y = v.find(".jqg-first-row-header"),
                    z = a.jgrid.styleUI[q.p.styleUI || "jQueryUI"].base;
                q.p.groupHeader || (q.p.groupHeader = []), q.p.groupHeader.push(b), void
                0 === y[0] ? y = a("<tr>", {
                    role: "row",
                    "aria-hidden": "true"
                }).addClass("jqg-first-row-header").css("height", "auto") : y.empty();
                var
                A, B = function (a, b) {
                    var
                    c, d = b.length;
                    for (c = 0; c < d; c++) if (b[c].startColumnName === a) return c;
                    return -1
                };
                for (a(q).prepend(x), e = a("<tr>", {
                    role: "row"
                }).addClass("ui-jqgrid-labels jqg-third-row-header"), c = 0; c < t; c++) if (g = u[c].el, h = a(g), d = s[c], i = {
                    height: "0px",
                    width: u[c].width + "px",
                    display: d.hidden ? "none" : ""
                }, a("<th>", {
                    role: "gridcell"
                }).css(i).addClass("ui-first-th-" + q.p.direction).appendTo(y), g.style.width = "", (j = B(d.name, b.groupHeaders)) >= 0) {
                    for (k = b.groupHeaders[j], l = k.numberOfColumns, m = k.titleText, o = k.className || "", n = 0, j = 0; j < l && c + j < t; j++) s[c + j].hidden || n++;
                    f = a("<th>").attr({
                        role: "columnheader"
                    }).addClass(z.headerBox + " ui-th-column-header ui-th-" + q.p.direction + " " + o).html(m), n > 0 && f.attr("colspan", String(n)), q.p.headertitles && f.attr("title", f.text()), 0 === n && f.hide(), h.before(f), e.append(g), r = l - 1
                } else if (0 === r) if (b.useColSpanStyle) {
                    var
                    C = h.attr("rowspan") ? parseInt(h.attr("rowspan"), 10) + 1 : 2;
                    h.attr("rowspan", C)
                } else a("<th>", {
                    role: "columnheader"
                }).addClass(z.headerBox + " ui-th-column-header ui-th-" + q.p.direction).css({
                    display: d.hidden ? "none" : ""
                }).insertBefore(h), e.append(g);
                else e.append(g), r--;
                p = a(q).children("thead"), p.prepend(y), e.insertAfter(w), v.append(p), b.useColSpanStyle && (v.find("span.ui-jqgrid-resize").each(function () {
                    var
                    b = a(this).parent();
                    b.is(":visible") && (this.style.cssText = "height: " + b.height() + "px !important; cursor: col-resize;")
                }), v.find("div.ui-jqgrid-sortable").each(function () {
                    var
                    b = a(this),
                        c = b.parent();
                    c.is(":visible") && c.is(":has(span.ui-jqgrid-resize)") && b.css("top", (c.height() - b.outerHeight()) / 2 - 4 + "px")
                })), A = p.find("tr.jqg-first-row-header"), a(q).on("jqGridResizeStop.setGroupHeaders", function (a, b, c) {
                    A.find("th").eq(c)[0].style.width = b + "px"
                })
            })
        },
        destroyGroupHeader: function (b) {
            return void
            0 === b && (b = !0), this.each(function () {
                var
                c, d, e, f, g, h, i, j = this,
                    k = j.grid,
                    l = a("table.ui-jqgrid-htable thead", k.hDiv),
                    m = j.p.colModel;
                if (k) {
                    for (a(this).off(".setGroupHeaders"), c = a("<tr>", {
                        role: "row"
                    }).addClass("ui-jqgrid-labels"), f = k.headers, d = 0, e = f.length; d < e; d++) {
                        i = m[d].hidden ? "none" : "", g = a(f[d].el).width(f[d].width).css("display", i);
                        try {
                            g.removeAttr("rowSpan")
                        } catch (a) {
                            g.attr("rowSpan", 1)
                        }
                        c.append(g), h = g.children("span.ui-jqgrid-resize"), h.length > 0 && (h[0].style.height = ""), g.children("div")[0].style.top = ""
                    }
                    a(l).children("tr.ui-jqgrid-labels").remove(), a(l).prepend(c), !0 === b && a(j).jqGrid("setGridParam", {
                        groupHeader: null
                    })
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid.extend({
        setTreeNode: function (b, c) {
            return this.each(function () {
                var
                d = this;
                if (d.grid && d.p.treeGrid) {
                    var
                    e, f, g, h, i, j, k, l, m = d.p.expColInd,
                        n = d.p.treeReader.expanded_field,
                        o = d.p.treeReader.leaf_field,
                        p = d.p.treeReader.level_field,
                        q = d.p.treeReader.icon_field,
                        r = d.p.treeReader.loaded,
                        s = a.jgrid.styleUI[d.p.styleUI || "jQueryUI"].common,
                        t = b;
                    for (a(d).triggerHandler("jqGridBeforeSetTreeNode", [t, c]), a.isFunction(d.p.beforeSetTreeNode) && d.p.beforeSetTreeNode.call(d, t, c); b < c;) {
                        var
                        u = a.jgrid.stripPref(d.p.idPrefix, d.rows[b].id),
                            v = d.p._index[u];
                        k = d.p.data[v], "nested" === d.p.treeGridModel && (k[o] || (e = parseInt(k[d.p.treeReader.left_field], 10), f = parseInt(k[d.p.treeReader.right_field], 10), k[o] = f === e + 1 ? "true" : "false", d.rows[b].cells[d.p._treeleafpos].innerHTML = k[o])), g = parseInt(k[p], 10), 0 === d.p.tree_root_level ? (h = g + 1, i = g) : (h = g, i = g - 1), j = "<div class='tree-wrap tree-wrap-" + d.p.direction + "' style='width:" + 18 * h + "px;'>", j += "<div style='" + ("rtl" === d.p.direction ? "right:" : "left:") + 18 * i + "px;' class='" + s.icon_base + " ", void
                        0 !== k[r] && ("true" === k[r] || !0 === k[r] ? k[r] = !0 : k[r] = !1), "true" === k[o] || !0 === k[o] ? (j += (void
                        0 !== k[q] && "" !== k[q] ? k[q] : d.p.treeIcons.leaf) + " tree-leaf treeclick", k[o] = !0, l = "leaf") : (k[o] = !1, l = ""), k[n] = ("true" === k[n] || !0 === k[n]) && (k[r] || void
                        0 === k[r]), !1 === k[n] ? j += !0 === k[o] ? "'" : d.p.treeIcons.plus + " tree-plus treeclick'" : j += !0 === k[o] ? "'" : d.p.treeIcons.minus + " tree-minus treeclick'", j += "></div></div>", a(d.rows[b].cells[m]).wrapInner("<span class='cell-wrapper" + l + "'></span>").prepend(j), g !== parseInt(d.p.tree_root_level, 10) && (a(d).jqGrid("isVisibleNode", k) || a(d.rows[b]).css("display", "none")), a(d.rows[b].cells[m]).find("div.treeclick").on("click", function (b) {
                            var
                            c = b.target || b.srcElement,
                                e = a.jgrid.stripPref(d.p.idPrefix, a(c, d.rows).closest("tr.jqgrow")[0].id),
                                f = d.p._index[e];
                            return d.p.data[f][o] || (d.p.data[f][n] ? (a(d).jqGrid("collapseRow", d.p.data[f]), a(d).jqGrid("collapseNode", d.p.data[f])) : (a(d).jqGrid("expandRow", d.p.data[f]), a(d).jqGrid("expandNode", d.p.data[f]))), !1
                        }), !0 === d.p.ExpandColClick && a(d.rows[b].cells[m]).find("span.cell-wrapper").css("cursor", "pointer").on("click", function (b) {
                            var
                            c = b.target || b.srcElement,
                                e = a.jgrid.stripPref(d.p.idPrefix, a(c, d.rows).closest("tr.jqgrow")[0].id),
                                f = d.p._index[e];
                            return d.p.data[f][o] || (d.p.data[f][n] ? (a(d).jqGrid("collapseRow", d.p.data[f]), a(d).jqGrid("collapseNode", d.p.data[f])) : (a(d).jqGrid("expandRow", d.p.data[f]), a(d).jqGrid("expandNode", d.p.data[f]))), a(d).jqGrid("setSelection", e), !1
                        }), b++
                    }
                    a(d).triggerHandler("jqGridAfterSetTreeNode", [t, c]), a.isFunction(d.p.afterSetTreeNode) && d.p.afterSetTreeNode.call(d, t, c)
                }
            })
        },
        setTreeGrid: function () {
            return this.each(function () {
                var
                b, c, d, e, f = this,
                    g = 0,
                    h = !1,
                    i = [],
                    j = a.jgrid.styleUI[f.p.styleUI || "jQueryUI"].treegrid;
                if (f.p.treeGrid) {
                    f.p.treedatatype || a.extend(f.p, {
                        treedatatype: f.p.datatype
                    }), f.p.loadonce && (f.p.treedatatype = "local"), f.p.subGrid = !1, f.p.altRows = !1, f.p.pgbuttons = !1, f.p.pginput = !1, f.p.gridview = !0, null === f.p.rowTotal && (f.p.rowNum = 1e4), f.p.multiselect = !1, f.p.rowList = [], f.p.expColInd = 0, b = j.icon_plus, "jQueryUI" === f.p.styleUI && (b += "rtl" === f.p.direction ? "w" : "e"), f.p.treeIcons = a.extend({
                        plus: b,
                        minus: j.icon_minus,
                        leaf: j.icon_leaf
                    }, f.p.treeIcons || {}), "nested" === f.p.treeGridModel ? f.p.treeReader = a.extend({
                        level_field: "level",
                        left_field: "lft",
                        right_field: "rgt",
                        leaf_field: "isLeaf",
                        expanded_field: "expanded",
                        loaded: "loaded",
                        icon_field: "icon"
                    }, f.p.treeReader) : "adjacency" === f.p.treeGridModel && (f.p.treeReader = a.extend({
                        level_field: "level",
                        parent_id_field: "parent",
                        leaf_field: "isLeaf",
                        expanded_field: "expanded",
                        loaded: "loaded",
                        icon_field: "icon"
                    }, f.p.treeReader));
                    for (d in f.p.colModel) if (f.p.colModel.hasOwnProperty(d)) {
                        c = f.p.colModel[d].name, c !== f.p.ExpandColumn || h || (h = !0, f.p.expColInd = g), g++;
                        for (e in f.p.treeReader) f.p.treeReader.hasOwnProperty(e) && f.p.treeReader[e] === c && i.push(c)
                    }
                    a.each(f.p.treeReader, function (b, c) {
                        c && -1 === a.inArray(c, i) && ("leaf_field" === b && (f.p._treeleafpos = g), g++, f.p.colNames.push(c), f.p.colModel.push({
                            name: c,
                            width: 1,
                            hidden: !0,
                            sortable: !1,
                            resizable: !1,
                            hidedlg: !0,
                            editable: !0,
                            search: !1
                        }))
                    })
                }
            })
        },
        expandRow: function (b) {
            this.each(function () {
                var
                c = this;
                if (c.grid && c.p.treeGrid) {
                    var
                    d = a(c).jqGrid("getNodeChildren", b),
                        e = c.p.treeReader.expanded_field,
                        f = b[c.p.localReader.id],
                        g = a(c).triggerHandler("jqGridBeforeExpandTreeGridRow", [f, b, d]);
                    void
                    0 === g && (g = !0), g && a.isFunction(c.p.beforeExpandTreeGridRow) && (g = c.p.beforeExpandTreeGridRow.call(c, f, b, d)), !1 !== g && (a(d).each(function () {
                        var
                        b = c.p.idPrefix + a.jgrid.getAccessor(this, c.p.localReader.id);
                        a(a(c).jqGrid("getGridRowById", b)).css("display", ""), this[e] && a(c).jqGrid("expandRow", this)
                    }), a(c).triggerHandler("jqGridAfterExpandTreeGridRow", [f, b, d]), a.isFunction(c.p.afterExpandTreeGridRow) && c.p.afterExpandTreeGridRow.call(c, f, b, d))
                }
            })
        },
        collapseRow: function (b) {
            this.each(function () {
                var
                c = this;
                if (c.grid && c.p.treeGrid) {
                    var
                    d = a(c).jqGrid("getNodeChildren", b),
                        e = c.p.treeReader.expanded_field,
                        f = b[c.p.localReader.id],
                        g = a(c).triggerHandler("jqGridBeforeCollapseTreeGridRow", [f, b, d]);
                    void
                    0 === g && (g = !0), g && a.isFunction(c.p.beforeCollapseTreeGridRow) && (g = c.p.beforeCollapseTreeGridRow.call(c, f, b, d)), !1 !== g && (a(d).each(function () {
                        var
                        b = c.p.idPrefix + a.jgrid.getAccessor(this, c.p.localReader.id);
                        a(a(c).jqGrid("getGridRowById", b)).css("display", "none"), this[e] && a(c).jqGrid("collapseRow", this)
                    }), a(c).triggerHandler("jqGridAfterCollapseTreeGridRow", [f, b, d]), a.isFunction(c.p.afterCollapseTreeGridRow) && c.p.afterCollapseTreeGridRow.call(c, f, b, d))
                }
            })
        },
        getRootNodes: function (b) {
            var
            c = [];
            return this.each(function () {
                var
                d, e, f, g = this;
                if (g.grid && g.p.treeGrid) switch ("boolean" != typeof
                b && (b = !1), f = b ? a(g).jqGrid("getRowData", null, !0) : g.p.data, g.p.treeGridModel) {
                    case "nested":
                        d = g.p.treeReader.level_field, a(f).each(function () {
                            parseInt(this[d], 10) === parseInt(g.p.tree_root_level, 10) && (b ? c.push(g.p.data[g.p._index[this[g.p.keyName]]]) : c.push(this))
                        });
                        break;
                    case "adjacency":
                        e = g.p.treeReader.parent_id_field, a(f).each(function () {
                            null !== this[e] && "null" !== String(this[e]).toLowerCase() || (b ? c.push(g.p.data[g.p._index[this[g.p.keyName]]]) : c.push(this))
                        })
                }
            }), c
        },
        getNodeDepth: function (b) {
            var
            c = null;
            return this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    var
                    d = this;
                    switch (d.p.treeGridModel) {
                        case "nested":
                            var
                            e = d.p.treeReader.level_field;
                            c = parseInt(b[e], 10) - parseInt(d.p.tree_root_level, 10);
                            break;
                        case "adjacency":
                            c = a(d).jqGrid("getNodeAncestors", b).length
                    }
                }
            }), c
        },
        getNodeParent: function (b) {
            var
            c = null;
            return this.each(function () {
                var
                d = this;
                if (d.grid && d.p.treeGrid) switch (d.p.treeGridModel) {
                    case "nested":
                        var
                        e = d.p.treeReader.left_field,
                            f = d.p.treeReader.right_field,
                            g = d.p.treeReader.level_field,
                            h = parseInt(b[e], 10),
                            i = parseInt(b[f], 10),
                            j = parseInt(b[g], 10);
                        a(this.p.data).each(function () {
                            if (parseInt(this[g], 10) === j - 1 && parseInt(this[e], 10) < h && parseInt(this[f], 10) > i) return c = this, !1
                        });
                        break;
                    case "adjacency":
                        for (var
                        k = d.p.treeReader.parent_id_field, l = d.p.localReader.id, m = b[l], n = d.p._index[m]; n--;) if (String(d.p.data[n][l]) === String(a.jgrid.stripPref(d.p.idPrefix, b[k]))) {
                            c = d.p.data[n];
                            break
                        }
                }
            }), c
        },
        getNodeChildren: function (b, c) {
            var
            d = [];
            return this.each(function () {
                var
                e = this;
                if (e.grid && e.p.treeGrid) {
                    var
                    f, g, h = c ? this.rows.length : this.p.data.length;
                    switch (e.p.treeGridModel) {
                        case "nested":
                            var
                            i = e.p.treeReader.left_field,
                                j = e.p.treeReader.right_field,
                                k = e.p.treeReader.level_field,
                                l = parseInt(b[i], 10),
                                m = parseInt(b[j], 10),
                                n = parseInt(b[k], 10);
                            for (f = 0; f < h; f++)(g = c ? e.p.data[e.p._index[this.rows[f].id]] : e.p.data[f]) && parseInt(g[k], 10) === n + 1 && parseInt(g[i], 10) > l && parseInt(g[j], 10) < m && d.push(g);
                            break;
                        case "adjacency":
                            var
                            o = e.p.treeReader.parent_id_field,
                                p = e.p.localReader.id;
                            for (f = 0; f < h; f++)(g = c ? e.p.data[e.p._index[this.rows[f].id]] : e.p.data[f]) && String(g[o]) === String(a.jgrid.stripPref(e.p.idPrefix, b[p])) && d.push(g)
                    }
                }
            }), d
        },
        getFullTreeNode: function (b, c) {
            var
            d = [];
            return this.each(function () {
                var
                e, f = this,
                    g = f.p.treeReader.expanded_field;
                if (f.grid && f.p.treeGrid) switch (null != c && "boolean" == typeof
                c || (c = !1), f.p.treeGridModel) {
                    case "nested":
                        var
                        h = f.p.treeReader.left_field,
                            i = f.p.treeReader.right_field,
                            j = f.p.treeReader.level_field,
                            k = parseInt(b[h], 10),
                            l = parseInt(b[i], 10),
                            m = parseInt(b[j], 10);
                        a(this.p.data).each(function () {
                            parseInt(this[j], 10) >= m && parseInt(this[h], 10) >= k && parseInt(this[h], 10) <= l && (c && (this[g] = !0), d.push(this))
                        });
                        break;
                    case "adjacency":
                        if (b) {
                            d.push(b);
                            var
                            n = f.p.treeReader.parent_id_field,
                                o = f.p.localReader.id;
                            a(this.p.data).each(function (b) {
                                for (e = d.length, b = 0; b < e; b++) if (String(a.jgrid.stripPref(f.p.idPrefix, d[b][o])) === String(this[n])) {
                                    c && (this[g] = !0), d.push(this);
                                    break
                                }
                            })
                        }
                }
            }), d
        },
        getNodeAncestors: function (b, c, d) {
            var
            e = [];
            return void
            0 === c && (c = !1), this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    d = void
                    0 !== d && this.p.treeReader.expanded_field;
                    for (var
                    f = a(this).jqGrid("getNodeParent", b); f;) {
                        if (d) try {
                            f[d] = !0
                        } catch (a) {}
                        c ? e.unshift(f) : e.push(f), f = a(this).jqGrid("getNodeParent", f)
                    }
                }
            }), e
        },
        isVisibleNode: function (b) {
            var
            c = !0;
            return this.each(function () {
                var
                d = this;
                if (d.grid && d.p.treeGrid) {
                    var
                    e = a(d).jqGrid("getNodeAncestors", b),
                        f = d.p.treeReader.expanded_field;
                    a(e).each(function () {
                        if (!(c = c && this[f])) return !1
                    })
                }
            }), c
        },
        isNodeLoaded: function (b) {
            var
            c;
            return this.each(function () {
                var
                d = this;
                if (d.grid && d.p.treeGrid) {
                    var
                    e = d.p.treeReader.leaf_field,
                        f = d.p.treeReader.loaded;
                    c = void
                    0 !== b && (void
                    0 !== b[f] ? b[f] : !! (b[e] || a(d).jqGrid("getNodeChildren", b).length > 0))
                }
            }), c
        },
        setLeaf: function (b, c, d) {
            return this.each(function () {
                var
                e = a.jgrid.getAccessor(b, this.p.localReader.id),
                    f = a("#" + e, this.grid.bDiv)[0],
                    g = this.p.treeReader.leaf_field;
                try {
                    var
                    h = this.p._index[e];
                    null != h && (this.p.data[h][g] = c)
                } catch (a) {}
                if (!0 === c) a("div.treeclick", f).removeClass(this.p.treeIcons.minus + " tree-minus " + this.p.treeIcons.plus + " tree-plus").addClass(this.p.treeIcons.leaf + " tree-leaf");
                else if (!1 === c) {
                    var
                    i = this.p.treeIcons.minus + " tree-minus";
                    d && (i = this.p.treeIcons.plus + " tree-plus"), a("div.treeclick", f).removeClass(this.p.treeIcons.leaf + " tree-leaf").addClass(i)
                }
            })
        },
        reloadNode: function (b, c) {
            return this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    var
                    d = this.p.localReader.id,
                        e = this.p.selrow;
                    a(this).jqGrid("delChildren", b[d]), void
                    0 === c && (c = !1), c || jQuery._data(this, "events").jqGridAfterSetTreeNode || a(this).on("jqGridAfterSetTreeNode.reloadNode", function () {
                        var
                        b = this.p.treeReader.leaf_field;
                        if (this.p.reloadnode) {
                            var
                            c = this.p.reloadnode,
                                d = a(this).jqGrid("getNodeChildren", c);
                            c[b] && d.length ? a(this).jqGrid("setLeaf", c, !1) : c[b] || 0 !== d.length || a(this).jqGrid("setLeaf", c, !0)
                        }
                        this.p.reloadnode = !1
                    });
                    var
                    f = this.p.treeReader.expanded_field,
                        g = this.p.treeReader.parent_id_field,
                        h = this.p.treeReader.loaded,
                        i = this.p.treeReader.level_field,
                        j = this.p.treeReader.leaf_field,
                        k = this.p.treeReader.left_field,
                        l = this.p.treeReader.right_field,
                        m = a.jgrid.getAccessor(b, this.p.localReader.id),
                        n = a("#" + m, this.grid.bDiv)[0];
                    b[f] = !0, b[j] || a("div.treeclick", n).removeClass(this.p.treeIcons.plus + " tree-plus").addClass(this.p.treeIcons.minus + " tree-minus"), this.p.treeANode = n.rowIndex, this.p.datatype = this.p.treedatatype, this.p.reloadnode = b, c && (this.p.treeANode = n.rowIndex > 0 ? n.rowIndex - 1 : 1, a(this).jqGrid("delRowData", m)), "nested" === this.p.treeGridModel ? a(this).jqGrid("setGridParam", {
                        postData: {
                            nodeid: m,
                            n_left: b[k],
                            n_right: b[l],
                            n_level: b[i]
                        }
                    }) : a(this).jqGrid("setGridParam", {
                        postData: {
                            nodeid: m,
                            parentid: b[g],
                            n_level: b[i]
                        }
                    }), a(this).trigger("reloadGrid"), b[h] = !0, "nested" === this.p.treeGridModel ? a(this).jqGrid("setGridParam", {
                        selrow: e,
                        postData: {
                            nodeid: "",
                            n_left: "",
                            n_right: "",
                            n_level: ""
                        }
                    }) : a(this).jqGrid("setGridParam", {
                        selrow: e,
                        postData: {
                            nodeid: "",
                            parentid: "",
                            n_level: ""
                        }
                    })
                }
            })
        },
        expandNode: function (b) {
            return this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    var
                    c = this,
                        d = this.p.treeReader.expanded_field,
                        e = this.p.treeReader.parent_id_field,
                        f = this.p.treeReader.loaded,
                        g = this.p.treeReader.level_field,
                        h = this.p.treeReader.left_field,
                        i = this.p.treeReader.right_field;
                    if (!b[d]) {
                        var
                        j = a.jgrid.getAccessor(b, this.p.localReader.id),
                            k = a("#" + this.p.idPrefix + a.jgrid.jqID(j), this.grid.bDiv)[0],
                            l = this.p._index[j],
                            m = a(c).triggerHandler("jqGridBeforeExpandTreeGridNode", [j, b]);
                        if (void
                        0 === m && (m = !0), m && a.isFunction(this.p.beforeExpandTreeGridNode) && (m = this.p.beforeExpandTreeGridNode.call(this, j, b)), !1 === m) return;
                        a(this).jqGrid("isNodeLoaded", this.p.data[l]) ? (b[d] = !0, a("div.treeclick", k).removeClass(this.p.treeIcons.plus + " tree-plus").addClass(this.p.treeIcons.minus + " tree-minus")) : this.grid.hDiv.loading || (b[d] = !0, a("div.treeclick", k).removeClass(this.p.treeIcons.plus + " tree-plus").addClass(this.p.treeIcons.minus + " tree-minus"), this.p.treeANode = k.rowIndex, this.p.datatype = this.p.treedatatype, "nested" === this.p.treeGridModel ? a(this).jqGrid("setGridParam", {
                            postData: {
                                nodeid: j,
                                n_left: b[h],
                                n_right: b[i],
                                n_level: b[g]
                            }
                        }) : a(this).jqGrid("setGridParam", {
                            postData: {
                                nodeid: j,
                                parentid: b[e],
                                n_level: b[g]
                            }
                        }), a(this).trigger("reloadGrid"), b[f] = !0, "nested" === this.p.treeGridModel ? a(this).jqGrid("setGridParam", {
                            postData: {
                                nodeid: "",
                                n_left: "",
                                n_right: "",
                                n_level: ""
                            }
                        }) : a(this).jqGrid("setGridParam", {
                            postData: {
                                nodeid: "",
                                parentid: "",
                                n_level: ""
                            }
                        })), a(c).triggerHandler("jqGridAfterExpandTreeGridNode", [j, b]), a.isFunction(this.p.afterExpandTreeGridNode) && this.p.afterExpandTreeGridNode.call(this, j, b)
                    }
                }
            })
        },
        collapseNode: function (b) {
            return this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    var
                    c = this.p.treeReader.expanded_field,
                        d = this;
                    if (b[c]) {
                        var
                        e = a.jgrid.getAccessor(b, this.p.localReader.id),
                            f = a("#" + this.p.idPrefix + a.jgrid.jqID(e), this.grid.bDiv)[0],
                            g = a(d).triggerHandler("jqGridBeforeCollapseTreeGridNode", [e, b]);
                        if (void
                        0 === g && (g = !0), g && a.isFunction(this.p.beforeCollapseTreeGridNode) && (g = this.p.beforeCollapseTreeGridNode.call(this, e, b)), b[c] = !1, !1 === g) return;
                        a("div.treeclick", f).removeClass(this.p.treeIcons.minus + " tree-minus").addClass(this.p.treeIcons.plus + " tree-plus"), a(d).triggerHandler("jqGridAfterCollapseTreeGridNode", [e, b]), a.isFunction(this.p.afterCollapseTreeGridNode) && this.p.afterCollapseTreeGridNode.call(this, e, b)
                    }
                }
            })
        },
        SortTree: function (b, c, d, e) {
            return this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    var
                    f, g, h, i, j, k = [],
                        l = this,
                        m = a(this).jqGrid("getRootNodes", l.p.search);
                    for (i = a.jgrid.from.call(this, m), i.orderBy(b, c, d, e), j = i.select(), f = 0, g = j.length; f < g; f++) h = j[f], k.push(h), a(this).jqGrid("collectChildrenSortTree", k, h, b, c, d, e);
                    a.each(k, function (b) {
                        var
                        c = a.jgrid.getAccessor(this, l.p.localReader.id);
                        a("#" + a.jgrid.jqID(l.p.id) + " tbody tr:eq(" + b + ")").after(a("tr#" + a.jgrid.jqID(c), l.grid.bDiv))
                    }), i = null, j = null, k = null
                }
            })
        },
        searchTree: function (b) {
            var
            c, d, e, f, g, h, i = b.length || 0,
                j = [],
                k = [],
                l = [];
            return this.each(function () {
                if (this.grid && this.p.treeGrid && i) for (c = this.p.localReader.id; i--;) if (j = a(this).jqGrid("getNodeAncestors", b[i], !0, !0), j.push(b[i]), d = j[0][c], -1 === a.inArray(d, k)) k.push(d), l = l.concat(j);
                else for (g = 0, e = j.length; g < e; g++) {
                    var
                    m = !1;
                    for (h = 0, f = l.length; h < f; h++) if (j[g][c] === l[h][c]) {
                        m = !0;
                        break
                    }
                    m || l.push(j[g])
                }
            }), l
        },
        collectChildrenSortTree: function (b, c, d, e, f, g) {
            return this.each(function () {
                if (this.grid && this.p.treeGrid) {
                    var
                    h, i, j, k, l, m;
                    for (k = a(this).jqGrid("getNodeChildren", c, this.p.search), l = a.jgrid.from.call(this, k), l.orderBy(d, e, f, g), m = l.select(), h = 0, i = m.length; h < i; h++) j = m[h], b.push(j), a(this).jqGrid("collectChildrenSortTree", b, j, d, e, f, g)
                }
            })
        },
        setTreeRow: function (b, c) {
            var
            d = !1;
            return this.each(function () {
                var
                e = this;
                e.grid && e.p.treeGrid && (d = a(e).jqGrid("setRowData", b, c))
            }), d
        },
        delTreeNode: function (b) {
            return this.each(function () {
                var
                c, d, e, f, g, h = this,
                    i = h.p.localReader.id,
                    j = h.p.treeReader.left_field,
                    k = h.p.treeReader.right_field;
                if (h.grid && h.p.treeGrid) {
                    var
                    l = h.p._index[b];
                    if (void
                    0 !== l) {
                        d = parseInt(h.p.data[l][k], 10), e = d - parseInt(h.p.data[l][j], 10) + 1;
                        var
                        m = a(h).jqGrid("getFullTreeNode", h.p.data[l]);
                        if (m.length > 0) for (c = 0; c < m.length; c++) a(h).jqGrid("delRowData", m[c][i]);
                        if ("nested" === h.p.treeGridModel) {
                            if (f = a.jgrid.from.call(h, h.p.data).greater(j, d, {
                                stype: "integer"
                            }).select(), f.length) for (g in f) f.hasOwnProperty(g) && (f[g][j] = parseInt(f[g][j], 10) - e);
                            if (f = a.jgrid.from.call(h, h.p.data).greater(k, d, {
                                stype: "integer"
                            }).select(), f.length) for (g in f) f.hasOwnProperty(g) && (f[g][k] = parseInt(f[g][k], 10) - e)
                        }
                    }
                }
            })
        },
        delChildren: function (b) {
            return this.each(function () {
                var
                c, d, e, f, g = this,
                    h = g.p.localReader.id,
                    i = g.p.treeReader.left_field,
                    j = g.p.treeReader.right_field;
                if (g.grid && g.p.treeGrid) {
                    var
                    k = g.p._index[b];
                    if (void
                    0 !== k) {
                        c = parseInt(g.p.data[k][j], 10), d = c - parseInt(g.p.data[k][i], 10) + 1;
                        var
                        l = a(g).jqGrid("getFullTreeNode", g.p.data[k]);
                        if (l.length > 0) for (var
                        m = 0; m < l.length; m++) l[m][h] !== b && a(g).jqGrid("delRowData", l[m][h]);
                        if ("nested" === g.p.treeGridModel) {
                            if (e = a.jgrid.from(g.p.data).greater(i, c, {
                                stype: "integer"
                            }).select(), e.length) for (f in e) e.hasOwnProperty(f) && (e[f][i] = parseInt(e[f][i], 10) - d);
                            if (e = a.jgrid.from(g.p.data).greater(j, c, {
                                stype: "integer"
                            }).select(), e.length) for (f in e) e.hasOwnProperty(f) && (e[f][j] = parseInt(e[f][j], 10) - d)
                        }
                    }
                }
            })
        },
        addChildNode: function (b, c, d, e) {
            var
            f = this[0];
            if (d) {
                var
                g, h, i, j, k, l, m, n, o = f.p.treeReader.expanded_field,
                    p = f.p.treeReader.leaf_field,
                    q = f.p.treeReader.level_field,
                    r = f.p.treeReader.parent_id_field,
                    s = f.p.treeReader.left_field,
                    t = f.p.treeReader.right_field,
                    u = f.p.treeReader.loaded,
                    v = 0,
                    w = c;
                if (void
                0 === e && (e = !1), null == b) {
                    if ((k = f.p.data.length - 1) >= 0) for (; k >= 0;) v = Math.max(v, parseInt(f.p.data[k][f.p.localReader.id], 10)), k--;
                    b = v + 1
                }
                var
                x = a(f).jqGrid("getInd", c);
                if (m = !1, void
                0 === c || null === c || "" === c) c = null, w = null, g = "last", j = f.p.tree_root_level, k = f.p.data.length + 1;
                else {
                    g = "after", h = f.p._index[c], i = f.p.data[h], c = i[f.p.localReader.id], j = parseInt(i[q], 10) + 1;
                    var
                    y = a(f).jqGrid("getFullTreeNode", i);
                    y.length ? (k = y[y.length - 1][f.p.localReader.id], w = k, k = a(f).jqGrid("getInd", w) + 1) : k = a(f).jqGrid("getInd", c) + 1, i[p] && (m = !0, i[o] = !0, a(f.rows[x]).find("span.cell-wrapperleaf").removeClass("cell-wrapperleaf").addClass("cell-wrapper").end().find("div.tree-leaf").removeClass(f.p.treeIcons.leaf + " tree-leaf").addClass(f.p.treeIcons.minus + " tree-minus"), f.p.data[h][p] = !1, i[u] = !0)
                }
                if (l = k + 1, void
                0 === d[o] && (d[o] = !1), void
                0 === d[u] && (d[u] = !1), d[q] = j, void
                0 === d[p] && (d[p] = !0), "adjacency" === f.p.treeGridModel && (d[r] = c), "nested" === f.p.treeGridModel) {
                    var
                    z, A, B;
                    if (null !== c) {
                        if (n = parseInt(i[t], 10), z = a.jgrid.from.call(f, f.p.data), z = z.greaterOrEquals(t, n, {
                            stype: "integer"
                        }), A = z.select(), A.length) for (B in A) A.hasOwnProperty(B) && (A[B][s] = A[B][s] > n ? parseInt(A[B][s], 10) + 2 : A[B][s], A[B][t] = A[B][t] >= n ? parseInt(A[B][t], 10) + 2 : A[B][t]);
                        d[s] = n, d[t] = n + 1
                    } else {
                        if (n = parseInt(a(f).jqGrid("getCol", t, !1, "max"), 10), A = a.jgrid.from.call(f, f.p.data).greater(s, n, {
                            stype: "integer"
                        }).select(), A.length) for (B in A) A.hasOwnProperty(B) && (A[B][s] = parseInt(A[B][s], 10) + 2);
                        if (A = a.jgrid.from.call(f, f.p.data).greater(t, n, {
                            stype: "integer"
                        }).select(), A.length) for (B in A) A.hasOwnProperty(B) && (A[B][t] = parseInt(A[B][t], 10) + 2);
                        d[s] = n + 1, d[t] = n + 2
                    }
                }(null === c || a(f).jqGrid("isNodeLoaded", i) || m) && (a(f).jqGrid("addRowData", b, d, g, w), a(f).jqGrid("setTreeNode", k, l)), i && !i[o] && e && a(f.rows[x]).find("div.treeclick").click()
            }
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "./grid.grouping"], a) : a(jQuery)
}(function (a) {
    "use strict";

    function
    b(a, b) {
        var
        c, d, e, f = [];
        if (!this || "function" != typeof
        a || a
        instanceof
        RegExp) throw new
        TypeError;
        for (e = this.length, c = 0; c < e; c++) if (this.hasOwnProperty(c) && (d = this[c], a.call(b, d, c, this))) {
            f.push(d);
            break
        }
        return f
    }
    a.assocArraySize = function (a) {
        var
        b, c = 0;
        for (b in a) a.hasOwnProperty(b) && c++;
        return c
    }, a.jgrid.extend({
        pivotSetup: function (c, d) {
            var
            e = [],
                f = [],
                g = [],
                h = [],
                i = [],
                j = {
                    grouping: !0,
                    groupingView: {
                        groupField: [],
                        groupSummary: [],
                        groupSummaryPos: []
                    }
                }, k = [],
                l = a.extend({
                    rowTotals: !1,
                    rowTotalsText: "Total",
                    colTotals: !1,
                    groupSummary: !0,
                    groupSummaryPos: "header",
                    frozenStaticCols: !1
                }, d || {});
            return this.each(function () {
                function
                d(a, c, d) {
                    var
                    e;
                    return e = b.call(a, c, d), e.length > 0 ? e[0] : null
                }

                function
                m(a, b) {
                    var
                    c, d = 0,
                        e = !0;
                    for (c in a) if (a.hasOwnProperty(c)) {
                        if (a[c] != this[d]) {
                            e = !1;
                            break
                        }
                        if (++d >= this.length) break
                    }
                    return e && (r = b), e
                }

                function
                n(b, c, d, e, f) {
                    var
                    g;
                    if (a.isFunction(b)) g = b.call(y, c, d, e);
                    else switch (b) {
                        case "sum":
                            g = parseFloat(c || 0) + parseFloat(e[d] || 0);
                            break;
                        case "count":
                                "" !== c && null != c || (c = 0), g = e.hasOwnProperty(d) ? c + 1 : 0;
                            break;
                        case "min":
                            g = "" === c || null == c ? parseFloat(e[d] || 0) : Math.min(parseFloat(c), parseFloat(e[d] || 0));
                            break;
                        case "max":
                            g = "" === c || null == c ? parseFloat(e[d] || 0) : Math.max(parseFloat(c), parseFloat(e[d] || 0));
                            break;
                        case "avg":
                            g = (parseFloat(c || 0) * (f - 1) + parseFloat(e[d] || 0)) / f
                    }
                    return g
                }

                function
                o(b, c, d, e) {
                    var
                    g, j, k, l, m, o, p = c.length,
                        q = "",
                        s = [],
                        t = 1;
                    for (a.isArray(d) ? (l = d.length, s = d) : (l = 1, s[0] = d), h = [], i = [], h.root = 0, k = 0; k < l; k++) {
                        var
                        u, v = [];
                        for (g = 0; g < p; g++) {
                            if (m = "string" == typeof
                            c[g].aggregator ? c[g].aggregator : "cust", null == d) j = a.trim(c[g].member) + "_" + m, u = j, s[0] = c[g].label || m + " " + a.trim(c[g].member);
                            else {
                                u = d[k].replace(/\s+/g, "");
                                try {
                                    j = 1 === p ? q + u : q + u + "_" + m + "_" + String(g)
                                } catch (a) {}
                                s[k] = d[k]
                            }
                            j = isNaN(parseInt(j, 10)) ? j : j + " ", "avg" === c[g].aggregator && (o = -1 === r ? f.length + "_" + j : r + "_" + j, F[o] ? F[o]++ : F[o] = 1, t = F[o]), e[j] = v[j] = n(c[g].aggregator, e[j], c[g].member, b, t)
                        }
                        q += d && null != d[k] ? d[k].replace(/\s+/g, "") : "", h[j] = v, i[j] = s[k]
                    }
                    return e
                }

                function
                p(a) {
                    var
                    b, c, d, f, g;
                    for (d in a) if (a.hasOwnProperty(d)) {
                        if ("object" != typeof
                        a[d]) {
                            if ("level" === d) {
                                if (void
                                0 === N[a.level] && (N[a.level] = "", a.level > 0 && -1 === a.text.indexOf("_r_Totals") && (k[a.level - 1] = {
                                    useColSpanStyle: !1,
                                    groupHeaders: []
                                })), N[a.level] !== a.text && a.children.length && -1 === a.text.indexOf("_r_Totals") && a.level > 0) {
                                    k[a.level - 1].groupHeaders.push({
                                        titleText: a.label,
                                        numberOfColumns: 0
                                    });
                                    var
                                    h = k[a.level - 1].groupHeaders.length - 1,
                                        i = 0 === h ? P : O;
                                    if (a.level - 1 == (l.rowTotals ? 1 : 0) && h > 0) {
                                        for (var
                                        j = 0, m = 0; m < h; m++) j += k[a.level - 1].groupHeaders[m].numberOfColumns;
                                        j && (i = j + t)
                                    }
                                    e[i] && (k[a.level - 1].groupHeaders[h].startColumnName = e[i].name, k[a.level - 1].groupHeaders[h].numberOfColumns = e.length - i), O = e.length
                                }
                                N[a.level] = a.text
                            }
                            if (a.level === u && "level" === d && u > 0) if (v > 1) {
                                var
                                n = 1;
                                for (b in a.fields) a.fields.hasOwnProperty(b) && (1 === n && k[u - 1].groupHeaders.push({
                                    startColumnName: b,
                                    numberOfColumns: 1,
                                    titleText: a.label || a.text
                                }), n++);
                                k[u - 1].groupHeaders[k[u - 1].groupHeaders.length - 1].numberOfColumns = n - 1
                            } else k.splice(u - 1, 1)
                        }
                        if (null != a[d] && "object" == typeof
                        a[d] && p(a[d]), "level" === d && a.level > 0 && (a.level === (0 === u ? a.level : u) || -1 !== N[a.level].indexOf("_r_Totals"))) {
                            c = 0;
                            for (b in a.fields) if (a.fields.hasOwnProperty(b)) {
                                g = {};
                                for (f in l.aggregates[c]) if (l.aggregates[c].hasOwnProperty(f)) switch (f) {
                                    case "member":
                                    case "label":
                                    case "aggregator":
                                        break;
                                    default:
                                        g[f] = l.aggregates[c][f]
                                }
                                v > 1 ? (g.name = b, g.label = l.aggregates[c].label || a.label) : (g.name = a.text, g.label = "_r_Totals" === a.text ? l.rowTotalsText : a.label), e.push(g), c++
                            }
                        }
                    }
                }
                var
                q, r, s, t, u, v, w, x, y = this,
                    z = c.length,
                    A = 0;
                if (l.rowTotals && l.yDimension.length > 0) {
                    var
                    B = l.yDimension[0].dataName;
                    l.yDimension.splice(0, 0, {
                        dataName: B
                    }), l.yDimension[0].converter = function () {
                        return "_r_Totals"
                    }
                }
                if (t = a.isArray(l.xDimension) ? l.xDimension.length : 0, u = l.yDimension.length, v = a.isArray(l.aggregates) ? l.aggregates.length : 0, 0 === t || 0 === v) throw "xDimension or aggregates optiona are not set!";
                var
                C;
                for (s = 0; s < t; s++) C = {
                    name: l.xDimension[s].dataName,
                    frozen: l.frozenStaticCols
                }, null == l.xDimension[s].isGroupField && (l.xDimension[s].isGroupField = !0), C = a.extend(!0, C, l.xDimension[s]), e.push(C);
                for (var
                D = t - 1, E = {}, F = []; A < z;) {
                    q = c[A];
                    var
                    G = [],
                        H = [];
                    w = {}, s = 0;
                    do {
                        G[s] = a.trim(q[l.xDimension[s].dataName]), w[l.xDimension[s].dataName] = G[s], s++
                    } while (s < t);
                    var
                    I = 0;
                    if (r = -1, x = d(f, m, G)) {
                        if (r >= 0) {
                            if (I = 0, u >= 1) {
                                for (I = 0; I < u; I++) H[I] = a.trim(q[l.yDimension[I].dataName]), l.yDimension[I].converter && a.isFunction(l.yDimension[I].converter) && (H[I] = l.yDimension[I].converter.call(this, H[I], G, H));
                                x = o(q, l.aggregates, H, x)
                            } else 0 === u && (x = o(q, l.aggregates, null, x));
                            f[r] = x
                        }
                    } else {
                        if (I = 0, u >= 1) {
                            for (I = 0; I < u; I++) H[I] = a.trim(q[l.yDimension[I].dataName]), l.yDimension[I].converter && a.isFunction(l.yDimension[I].converter) && (H[I] = l.yDimension[I].converter.call(this, H[I], G, H));
                            w = o(q, l.aggregates, H, w)
                        } else 0 === u && (w = o(q, l.aggregates, null, w));
                        f.push(w)
                    }
                    var
                    J, K = 0,
                        L = null,
                        M = null;
                    for (J in h) if (h.hasOwnProperty(J)) {
                        if (0 === K) E.children && void
                        0 !== E.children || (E = {
                            text: J,
                            level: 0,
                            children: [],
                            label: J
                        }), L = E.children;
                        else {
                            for (M = null, s = 0; s < L.length; s++) if (L[s].text === J) {
                                M = L[s];
                                break
                            }
                            M ? L = M.children : (L.push({
                                children: [],
                                text: J,
                                level: K,
                                fields: h[J],
                                label: i[J]
                            }), L = L[L.length - 1].children)
                        }
                        K++
                    }
                    A++
                }
                F = null;
                var
                N = [],
                    O = e.length,
                    P = O;
                u > 0 && (k[u - 1] = {
                    useColSpanStyle: !1,
                    groupHeaders: []
                }), p(E);
                var
                Q;
                if (l.colTotals) for (var
                R = f.length; R--;) for (s = t; s < e.length; s++) Q = e[s].name, g[Q] ? g[Q] += parseFloat(f[R][Q] || 0) : g[Q] = parseFloat(f[R][Q] || 0);
                if (D > 0) for (s = 0; s < D; s++) e[s].isGroupField && (j.groupingView.groupField.push(e[s].name), j.groupingView.groupSummary.push(l.groupSummary), j.groupingView.groupSummaryPos.push(l.groupSummaryPos));
                else j.grouping = !1;
                j.sortname = e[D].name, j.groupingView.hideFirstGroupCol = !0
            }), {
                colModel: e,
                rows: f,
                groupOptions: j,
                groupHeaders: k,
                summary: g
            }
        },
        jqPivot: function (b, c, d, e) {
            return this.each(function () {
                function
                f(b) {
                    if (!a.isArray(b)) throw "data provides is not an array";
                    var
                    e, f, h, i, j = jQuery(g).jqGrid("pivotSetup", b, c),
                        k = a.assocArraySize(j.summary) > 0,
                        l = a.jgrid.from.call(g, j.rows);
                    for (c.ignoreCase && (l = l.ignoreCase()), e = 0; e < j.groupOptions.groupingView.groupField.length; e++) f = c.xDimension[e].sortorder ? c.xDimension[e].sortorder : "asc", h = c.xDimension[e].sorttype ? c.xDimension[e].sorttype : "text", l.orderBy(j.groupOptions.groupingView.groupField[e], f, h, "", h);
                    if (i = c.xDimension.length, d.sortname) {
                        for (f = d.sortorder ? d.sortorder : "asc", h = "text", e = 0; e < i; e++) if (c.xDimension[e].dataName === d.sortname) {
                            h = c.xDimension[e].sorttype ? c.xDimension[e].sorttype : "text";
                            break
                        }
                        l.orderBy(d.sortname, f, h, "", h)
                    } else j.groupOptions.sortname && i && (f = c.xDimension[i - 1].sortorder ? c.xDimension[i - 1].sortorder : "asc", h = c.xDimension[i - 1].sorttype ? c.xDimension[i - 1].sorttype : "text", l.orderBy(j.groupOptions.sortname, f, h, "", h));
                    jQuery(g).jqGrid(a.extend(!0, {
                        datastr: a.extend(l.select(), k ? {
                            userdata: j.summary
                        } : {}),
                        datatype: "jsonstring",
                        footerrow: k,
                        userDataOnFooter: k,
                        colModel: j.colModel,
                        viewrecords: !0,
                        sortname: c.xDimension[0].dataName
                    }, j.groupOptions, d || {}));
                    var
                    m = j.groupHeaders;
                    if (m.length) for (e = 0; e < m.length; e++) m[e] && m[e].groupHeaders.length && jQuery(g).jqGrid("setGroupHeaders", m[e]);
                    c.frozenStaticCols && jQuery(g).jqGrid("setFrozenColumns")
                }
                var
                g = this;
                "string" == typeof
                b ? a.ajax(a.extend({
                    url: b,
                    dataType: "json",
                    success: function (b) {
                        f(a.jgrid.getAccessor(b, e && e.reader ? e.reader : "rows"))
                    }
                }, e || {})) : f(b)
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.utils", "./grid.base"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid = a.jgrid || {}, a.extend(a.jgrid, {
        saveState: function (b, c) {
            if (c = a.extend({
                useStorage: !0,
                storageType: "localStorage",
                beforeSetItem: null,
                compression: !1,
                compressionModule: "LZString",
                compressionMethod: "compressToUTF16",
                debug: !1,
                saveData: !0
            }, c || {}), b) {
                var
                d, e, f = "",
                    g = "",
                    h = a("#" + b)[0];
                if (h.grid) {
                    if (e = a(h).data("inlineNav"), e && h.p.inlineNav && a(h).jqGrid("setGridParam", {
                        _iN: e
                    }), e = a(h).data("filterToolbar"), e && h.p.filterToolbar && a(h).jqGrid("setGridParam", {
                        _fT: e
                    }), f = a(h).jqGrid("jqGridExport", {
                        exptype: "jsonstring",
                        ident: "",
                        root: ""
                    }), g = "", c.saveData) {
                        g = a(h.grid.bDiv).find(".ui-jqgrid-btable tbody:first").html();
                        var
                        i = g.indexOf("</tr>");
                        g = g.slice(i + 5)
                    }
                    if (a.isFunction(c.beforeSetItem) && null != (d = c.beforeSetItem.call(h, f)) && (f = d), c.debug) {
                        a("#gbox_tree").prepend('<a id="link_save" target="_blank" download="jqGrid_dump.txt">Click to save Dump Data</a>');
                        var
                        j, k, l = [],
                            m = {};
                        l.push("Grid Options\n"), l.push(f), l.push("\n"), l.push("GridData\n"), l.push(g), m.type = "plain/text;charset=utf-8";
                        try {
                            j = new
                            File(l, "jqGrid_dump.txt", m)
                        } catch (a) {
                            j = new
                            Blob(l, m)
                        }
                        k = URL.createObjectURL(j), a("#link_save").attr("href", k).on("click", function () {
                            a(this).remove()
                        })
                    }
                    if (c.compression && c.compressionModule) try {
                        d = window[c.compressionModule][c.compressionMethod](f), null != d && (f = d, g = window[c.compressionModule][c.compressionMethod](g))
                    } catch (a) {}
                    if (c.useStorage && a.jgrid.isLocalStorage()) try {
                        window[c.storageType].setItem("jqGrid" + h.p.id, f), window[c.storageType].setItem("jqGrid" + h.p.id + "_data", g)
                    } catch (a) {
                        22 === a.code && alert("Local storage limit is over!")
                    }
                    return f
                }
            }
        },
        loadState: function (b, c, d) {
            if (d = a.extend({
                useStorage: !0,
                storageType: "localStorage",
                clearAfterLoad: !1,
                beforeSetGrid: null,
                afterSetGrid: null,
                decompression: !1,
                decompressionModule: "LZString",
                decompressionMethod: "decompressFromUTF16",
                restoreData: !0
            }, d || {}), b) {
                var
                e, f, g, h, i, j = a("#" + b)[0];
                if (d.useStorage) try {
                    c = window[d.storageType].getItem("jqGrid" + j.id), g = window[d.storageType].getItem("jqGrid" + j.id + "_data")
                } catch (a) {}
                if (c) {
                    if (d.decompression && d.decompressionModule) try {
                        e = window[d.decompressionModule][d.decompressionMethod](c), null != e && (c = e, g = window[d.decompressionModule][d.decompressionMethod](g))
                    } catch (a) {}
                    if ((e = a.jgrid.parseFunc(c)) && "object" === a.type(e)) {
                        j.grid && a.jgrid.gridUnload(b), a.isFunction(d.beforeSetGrid) && (f = d.beforeSetGrid(e)) && "object" === a.type(f) && (e = f);
                        var
                        k = function (a) {
                            return a
                        }, l = {
                            reccount: e.reccount,
                            records: e.records,
                            lastpage: e.lastpage,
                            shrinkToFit: k(e.shrinkToFit),
                            data: k(e.data),
                            datatype: k(e.datatype),
                            grouping: k(e.grouping)
                        };
                        e.shrinkToFit = !1, e.data = [], e.datatype = "local", e.grouping = !1, e.inlineNav && (h = k(e._iN), e._iN = null, delete
                        e._iN), e.filterToolbar && (i = k(e._fT), e._fT = null, delete
                        e._fT);
                        var
                        m = a("#" + b).jqGrid(e);
                        if (d.restoreData && "" !== a.trim(g) && m.append(g), m.jqGrid("setGridParam", l), e.storeNavOptions && e.navGrid && (m[0].p.navGrid = !1, m.jqGrid("navGrid", e.pager, e.navOptions, e.editOptions, e.addOptions, e.delOptions, e.searchOptions, e.viewOptions), e.navButtons && e.navButtons.length)) for (var
                        n = 0; n < e.navButtons.length; n++) "sepclass" in e.navButtons[n][1] ? m.jqGrid("navSeparatorAdd", e.navButtons[n][0], e.navButtons[n][1]) : m.jqGrid("navButtonAdd", e.navButtons[n][0], e.navButtons[n][1]);
                        if (m[0].refreshIndex(), e.subGrid) {
                            var
                            o = 1 === e.multiselect ? 1 : 0,
                                p = !0 === e.rownumbers ? 1 : 0;
                            m.jqGrid("addSubGrid", o + p)
                        }
                        if (e.treeGrid) for (var
                        q = 1, r = m[0].rows.length, s = e.expColInd, t = e.treeReader.leaf_field, u = e.treeReader.expanded_field; q < r;) a(m[0].rows[q].cells[s]).find("div.treeclick").on("click", function (b) {
                            var
                            c = b.target || b.srcElement,
                                d = a.jgrid.stripPref(e.idPrefix, a(c, m[0].rows).closest("tr.jqgrow")[0].id),
                                f = m[0].p._index[d];
                            return m[0].p.data[f][t] || (m[0].p.data[f][u] ? (m.jqGrid("collapseRow", m[0].p.data[f]), m.jqGrid("collapseNode", m[0].p.data[f])) : (m.jqGrid("expandRow", m[0].p.data[f]), m.jqGrid("expandNode", m[0].p.data[f]))), !1
                        }), !0 === e.ExpandColClick && a(m[0].rows[q].cells[s]).find("span.cell-wrapper").css("cursor", "pointer").on("click", function (b) {
                            var
                            c = b.target || b.srcElement,
                                d = a.jgrid.stripPref(e.idPrefix, a(c, m[0].rows).closest("tr.jqgrow")[0].id),
                                f = m[0].p._index[d];
                            return m[0].p.data[f][t] || (m[0].p.data[f][u] ? (m.jqGrid("collapseRow", m[0].p.data[f]), m.jqGrid("collapseNode", m[0].p.data[f])) : (m.jqGrid("expandRow", m[0].p.data[f]), m.jqGrid("expandNode", m[0].p.data[f]))), m.jqGrid("setSelection", d), !1
                        }), q++;
                        e.multiselect && a.each(e.selarrrow, function () {
                            a("#jqg_" + b + "_" + this)[e.useProp ? "prop" : "attr"]("checked", "checked")
                        }), e.inlineNav && h && (m.jqGrid("setGridParam", {
                            inlineNav: !1
                        }), m.jqGrid("inlineNav", e.pager, h)), e.filterToolbar && i && (m.jqGrid("setGridParam", {
                            filterToolbar: !1
                        }), i.restoreFromFilters = !0, m.jqGrid("filterToolbar", i)), e.frozenColumns && m.jqGrid("setFrozenColumns"), m[0].updatepager(!0, !0), a.isFunction(d.afterSetGrid) && d.afterSetGrid(m), d.clearAfterLoad && (window[d.storageType].removeItem("jqGrid" + j.id), window[d.storageType].removeItem("jqGrid" + j.id + "_data"))
                    } else alert("can not convert to object")
                }
            }
        },
        isGridInStorage: function (b, c) {
            var
            d = {
                storageType: "localStorage"
            };
            d = a.extend(d, c || {});
            var
            e, f, g;
            try {
                f = window[d.storageType].getItem("jqGrid" + b), g = window[d.storageType].getItem("jqGrid" + b + "_data"), e = null != f && null != g && "string" == typeof
                f && "string" == typeof
                g
            } catch (a) {
                e = !1
            }
            return e
        },
        setRegional: function (b, c) {
            var
            d = {
                storageType: "sessionStorage"
            };
            if (d = a.extend(d, c || {}), d.regional) {
                a.jgrid.saveState(b, d), d.beforeSetGrid = function (a) {
                    return a.regional = d.regional, a.force_regional = !0, a
                }, a.jgrid.loadState(b, null, d);
                var
                e = a("#" + b)[0],
                    f = a(e).jqGrid("getGridParam", "colModel"),
                    g = -1,
                    h = a.jgrid.getRegional(e, "nav");
                a.each(f, function (a) {
                    if (this.formatter && "actions" === this.formatter) return g = a, !1
                }), -1 !== g && h && a("#" + b + " tbody tr").each(function () {
                    var
                    b = this.cells[g];
                    a(b).find(".ui-inline-edit").attr("title", h.edittitle), a(b).find(".ui-inline-del").attr("title", h.deltitle), a(b).find(".ui-inline-save").attr("title", h.savetitle), a(b).find(".ui-inline-cancel").attr("title", h.canceltitle)
                });
                try {
                    window[d.storageType].removeItem("jqGrid" + e.id), window[d.storageType].removeItem("jqGrid" + e.id + "_data")
                } catch (a) {}
            }
        },
        jqGridImport: function (b, c) {
            c = a.extend({
                imptype: "xml",
                impstring: "",
                impurl: "",
                mtype: "GET",
                impData: {},
                xmlGrid: {
                    config: "root>grid",
                    data: "root>rows"
                },
                jsonGrid: {
                    config: "grid",
                    data: "data"
                },
                ajaxOptions: {}
            }, c || {});
            var
            d = (0 === b.indexOf("#") ? "" : "#") + a.jgrid.jqID(b),
                e = function (b, c) {
                    var
                    e, f, g, h = a(c.xmlGrid.config, b)[0],
                        i = a(c.xmlGrid.data, b)[0];
                    if (a.grid.xmlToJSON) {
                        e = a.jgrid.xmlToJSON(h);
                        for (g in e) e.hasOwnProperty(g) && (f = e[g]);
                        if (i) {
                            var
                            j = e.grid.datatype;
                            e.grid.datatype = "xmlstring", e.grid.datastr = b, a(d).jqGrid(f).jqGrid("setGridParam", {
                                datatype: j
                            })
                        } else setTimeout(function () {
                            a(d).jqGrid(f)
                        }, 0)
                    } else alert("xml2json or parse are not present")
                }, f = function (b, c) {
                    if (b && "string" == typeof
                    b) {
                        var
                        e = a.jgrid.parseFunc(b),
                            f = e[c.jsonGrid.config],
                            g = e[c.jsonGrid.data];
                        if (g) {
                            var
                            h = f.datatype;
                            f.datatype = "jsonstring", f.datastr = g, a(d).jqGrid(f).jqGrid("setGridParam", {
                                datatype: h
                            })
                        } else a(d).jqGrid(f)
                    }
                };
            switch (c.imptype) {
                case "xml":
                    a.ajax(a.extend({
                        url: c.impurl,
                        type: c.mtype,
                        data: c.impData,
                        dataType: "xml",
                        complete: function (b, f) {
                            "success" === f && (e(b.responseXML, c), a(d).triggerHandler("jqGridImportComplete", [b, c]), a.isFunction(c.importComplete) && c.importComplete(b)), b = null
                        }
                    }, c.ajaxOptions));
                    break;
                case "xmlstring":
                    if (c.impstring && "string" == typeof
                    c.impstring) {
                        var
                        g = a.parseXML(c.impstring);
                        g && (e(g, c), a(d).triggerHandler("jqGridImportComplete", [g, c]), a.isFunction(c.importComplete) && c.importComplete(g))
                    }
                    break;
                case "json":
                    a.ajax(a.extend({
                        url: c.impurl,
                        type: c.mtype,
                        data: c.impData,
                        dataType: "json",
                        complete: function (b) {
                            try {
                                f(b.responseText, c), a(d).triggerHandler("jqGridImportComplete", [b, c]), a.isFunction(c.importComplete) && c.importComplete(b)
                            } catch (a) {}
                            b = null
                        }
                    }, c.ajaxOptions));
                    break;
                case "jsonstring":
                    c.impstring && "string" == typeof
                    c.impstring && (f(c.impstring, c), a(d).triggerHandler("jqGridImportComplete", [c.impstring, c]), a.isFunction(c.importComplete) && c.importComplete(c.impstring))
            }
        }
    }), a.jgrid.extend({
        jqGridExport: function (b) {
            b = a.extend({
                exptype: "xmlstring",
                root: "grid",
                ident: "\t",
                addOptions: {}
            }, b || {});
            var
            c = null;
            return this.each(function () {
                if (this.grid) {
                    var
                    d = a.extend(!0, {}, a(this).jqGrid("getGridParam"), b.addOptions);
                    switch (d.rownumbers && (d.colNames.splice(0, 1), d.colModel.splice(0, 1)), d.multiselect && (d.colNames.splice(0, 1), d.colModel.splice(0, 1)), d.subGrid && (d.colNames.splice(0, 1), d.colModel.splice(0, 1)), d.knv = null, b.exptype) {
                        case "xmlstring":
                            c = "<" + b.root + ">" + a.jgrid.jsonToXML(d, {
                                xmlDecl: ""
                            }) + "</" + b.root + ">";
                            break;
                        case "jsonstring":
                            c = a.jgrid.stringify(d), b.root && (c = "{" + b.root + ":" + c + "}")
                    }
                }
            }), c
        },
        excelExport: function (b) {
            return b = a.extend({
                exptype: "remote",
                url: null,
                oper: "oper",
                tag: "excel",
                beforeExport: null,
                exporthidden: !1,
                exportgrouping: !1,
                exportOptions: {}
            }, b || {}), this.each(function () {
                if (this.grid) {
                    var
                    c;
                    if ("remote" === b.exptype) {
                        var
                        d, e = a.extend({}, this.p.postData);
                        if (e[b.oper] = b.tag, a.isFunction(b.beforeExport)) {
                            var
                            f = b.beforeExport.call(this, e);
                            a.isPlainObject(f) && (e = f)
                        }
                        if (b.exporthidden) {
                            var
                            g, h = this.p.colModel,
                                i = h.length,
                                j = [];
                            for (g = 0; g < i; g++) void
                            0 === h[g].hidden && (h[g].hidden = !1), j.push({
                                name: h[g].name,
                                hidden: h[g].hidden
                            });
                            var
                            k = JSON.stringify(j);
                            "string" == typeof
                            k && (e.colModel = k)
                        }
                        b.exportgrouping && "string" == typeof (d = JSON.stringify(this.p.groupingView)) && (e.groupingView = d);
                        var
                        l = jQuery.param(e);
                        c = -1 !== b.url.indexOf("?") ? b.url + "&" + l : b.url + "?" + l, window.location = c
                    }
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "./jquery.fmatter", "./grid.utils"], a) : a(jQuery)
}(function (a) {
    "use strict";
    a.jgrid = a.jgrid || {}, a.extend(a.jgrid, {
        formatCell: function (b, c, d, e, f) {
            var
            g;
            if (void
            0 !== e.formatter) {
                var
                h = {
                    rowId: "",
                    colModel: e,
                    gid: f.p.id,
                    pos: c,
                    styleUI: ""
                };
                g = a.isFunction(e.formatter) ? e.formatter.call(f, b, h, d) : a.fmatter ? a.fn.fmatter.call(f, e.formatter, b, h, d) : b
            } else g = b;
            return g
        },
        formatCellCsv: function (a, b) {
            a = null == a ? "" : String(a);
            try {
                a = a.replace(b._regexsep, b.separatorReplace).replace(/\r\n/g, b.replaceNewLine).replace(/\n/g, b.replaceNewLine)
            } catch (b) {
                a = ""
            }
            return b.escquote && (a = a.replace(b._regexquot, b.escquote + b.quote)), -1 !== a.indexOf(b.separator) && -1 !== a.indexOf(b.qoute) || (a = b.quote + a + b.quote), a
        },
        excelCellPos: function (a) {
            for (var
            b = "A".charCodeAt(0), c = "Z".charCodeAt(0), d = c - b + 1, e = ""; a >= 0;) e = String.fromCharCode(a % d + b) + e, a = Math.floor(a / d) - 1;
            return e
        },
        makeNode: function (b, c, d) {
            var
            e = b.createElement(c);
            return d && (d.attr && a(e).attr(d.attr), d.children && a.each(d.children, function (a, b) {
                e.appendChild(b)
            }), d.text && e.appendChild(b.createTextNode(d.text))), e
        },
        xmlToZip: function (b, c) {
            var
            d, e, f, g, h, i, j = this,
                k = new
                XMLSerializer,
                l = -1 === k.serializeToString(a.parseXML(a.jgrid.excelStrings["xl/worksheets/sheet1.xml"])).indexOf("xmlns:r"),
                m = [];
            a.each(c, function (c, n) {
                if (a.isPlainObject(n)) d = b.folder(c), j.xmlToZip(d, n);
                else {
                    if (l) {
                        for (e = n.childNodes[0], f = e.attributes.length - 1; f >= 0; f--) {
                            var
                            o = e.attributes[f].nodeName,
                                p = e.attributes[f].nodeValue; - 1 !== o.indexOf(":") && (m.push({
                                name: o,
                                value: p
                            }), e.removeAttribute(o))
                        }
                        for (f = 0, g = m.length; f < g; f++) h = n.createAttribute(m[f].name.replace(":", "_dt_b_namespace_token_")), h.value = m[f].value, e.setAttributeNode(h)
                    }
                    i = k.serializeToString(n), l && (-1 === i.indexOf("<?xml") && (i = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + i), i = i.replace(/_dt_b_namespace_token_/g, ":")), i = i.replace(/<row xmlns="" /g, "<row ").replace(/<cols xmlns="">/g, "<cols>").replace(/<mergeCells xmlns="" /g, "<mergeCells "), b.file(c, i)
                }
            })
        },
        excelStrings: {
            "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http:?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
            "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/xml" /><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" /><Default Extension="jpeg" ContentType="image/jpeg" /><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml" /><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml" /><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml" /></Types>',
            "xl/workbook.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><fileVersion appName="xl" lastEdited="5" lowestEdited="5" rupBuild="24816"/><workbookPr showInkAnnotation="0" autoCompressPictures="0"/><bookViews><workbookView xWindow="0" yWindow="0" windowWidth="25600" windowHeight="19020" tabRatio="500"/></bookViews><sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>',
            "xl/worksheets/sheet1.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"><sheetData/></worksheet>',
            "xl/styles.xml": '<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"><fonts count="5" x14ac:knownFonts="1"><font><sz val="11" /><name val="Calibri" /></font><font><sz val="11" /><name val="Calibri" /><color rgb="FFFFFFFF" /></font><font><sz val="11" /><name val="Calibri" /><b /></font><font><sz val="11" /><name val="Calibri" /><i /></font><font><sz val="11" /><name val="Calibri" /><u /></font></fonts><fills count="6"><fill><patternFill patternType="none" /></fill><fill/><fill><patternFill patternType="solid"><fgColor rgb="FFD9D9D9" /><bgColor indexed="64" /></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFD99795" /><bgColor indexed="64" /></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="ffc6efce" /><bgColor indexed="64" /></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="ffc6cfef" /><bgColor indexed="64" /></patternFill></fill></fills><borders count="2"><border><left /><right /><top /><bottom /><diagonal /></border><border diagonalUp="false" diagonalDown="false"><left style="thin"><color auto="1" /></left><right style="thin"><color auto="1" /></right><top style="thin"><color auto="1" /></top><bottom style="thin"><color auto="1" /></bottom><diagonal /></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" /></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment horizontal="center" /></xf><xf numFmtId="0" fontId="3" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="2" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="2" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="2" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="2" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="4" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="5" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="5" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="5" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="5" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="5" borderId="0" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="0" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="0" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="0" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="0" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="0" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="2" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="2" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="2" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="2" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="2" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="3" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="3" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="3" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="3" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="3" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="4" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="4" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="4" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="4" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="4" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="5" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="5" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="2" fillId="5" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="3" fillId="5" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/><xf numFmtId="0" fontId="4" fillId="5" borderId="1" applyFont="1" applyFill="1" applyBorder="1"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0" /></cellStyles><dxfs count="0" /><tableStyles count="0" defaultTableStyle="TableStyleMedium9" defaultPivotStyle="PivotStyleMedium4" /></styleSheet>'
        }
    }), a.jgrid.extend({
        exportToCsv: function (b) {
            b = a.extend(!0, {
                separator: ",",
                separatorReplace: " ",
                quote: '"',
                escquote: '"',
                newLine: "\r\n",
                replaceNewLine: " ",
                includeCaption: !0,
                includeLabels: !0,
                includeGroupHeader: !0,
                includeFooter: !0,
                fileName: "jqGridExport.csv",
                mimetype: "text/csv;charset=utf-8",
                returnAsString: !1
            }, b || {});
            var
            c = "";
            if (this.each(function () {
                function
                d(b, c) {
                    function
                    d(a, b, c) {
                        var
                        d, e = !1;
                        if (0 === b) e = c[a];
                        else {
                            var
                            f = c[a].idx;
                            if (0 === f) e = c[a];
                            else for (d = a; d >= 0; d--) if (c[d].idx === f - b) {
                                e = c[d];
                                break
                            }
                        }
                        return e
                    }

                    function
                    e(b, e, f, g) {
                        var
                        h, i, m = d(b, e, f),
                            n = m.cnt,
                            o = new
                            Array(c.collen),
                            p = 0;
                        for (i = g; i < l; i++) if (!k[i].hidden) {
                            var
                            q = "{0}";
                            a.each(m.summary, function () {
                                if (this.nm === k[i].name) {
                                    k[i].summaryTpl && (q = k[i].summaryTpl), "string" == typeof
                                    this.st && "avg" === this.st.toLowerCase() && (this.sd && this.vd ? this.v = this.v / this.vd : this.v && n > 0 && (this.v = this.v / n));
                                    try {
                                        this.groupCount = m.cnt, this.groupIndex = m.dataIndex, this.groupValue = m.value, h = j.formatter("", this.v, i, this)
                                    } catch (a) {
                                        h = this.v
                                    }
                                    return o[p] = a.jgrid.formatCellCsv(a.jgrid.stripHtml(a.jgrid.template(q, h)), c), !1
                                }
                            }), p++
                        }
                        return o
                    }
                    var
                    f = "",
                        g = j.p.groupingView,
                        h = [],
                        i = g.groupField.length,
                        k = j.p.colModel,
                        l = k.length,
                        m = 0;
                    a.each(k, function (a, b) {
                        var
                        c;
                        for (c = 0; c < i; c++) if (g.groupField[c] === b.name) {
                            h[c] = a;
                            break
                        }
                    });
                    var
                    n, o, p = a.makeArray(g.groupSummary);
                    return p.reverse(), a.each(g.groups, function (d, l) {
                        m++;
                        try {
                            n = a.isArray(g.formatDisplayField) && a.isFunction(g.formatDisplayField[l.idx]) ? g.formatDisplayField[l.idx].call(j, l.displayValue, l.value, j.p.colModel[h[l.idx]], l.idx, g) : j.formatter("", l.displayValue, h[l.idx], l.value)
                        } catch (a) {
                            n = l.displayValue
                        }
                        var
                        q = "";
                        "string" != typeof (q = a.isFunction(g.groupText[l.idx]) ? g.groupText[l.idx].call(j, n, l.cnt, l.summary) : a.jgrid.template(g.groupText[l.idx], n, l.cnt, l.summary)) && "number" != typeof
                        q && (q = n);
                        var
                        r;
                        if (r = "header" === g.groupSummaryPos[l.idx] ? e(d, 0, g.groups, 0) : new
                        Array(c.collen), r[0] = a.jgrid.formatCellCsv(a.jgrid.stripHtml(q), c), f += r.join(c.separator) + c.newLine, i - 1 === l.idx) {
                            var
                            s, t, u, v = g.groups[d + 1],
                                w = 0,
                                x = l.startRow,
                                y = void
                                0 !== v ? v.startRow : g.groups[d].startRow + g.groups[d].cnt;
                            for (s = x; s < y && b[s - w]; s++) {
                                for (u = b[s - w], o = 0, t = 0; t < k.length; t++) k[t].hidden || (r[o] = a.jgrid.formatCellCsv(a.jgrid.formatCell(u[k[t].name], t, u, k[t], j), c), o++);
                                f += r.join(c.separator) + c.newLine
                            }
                            if ("header" !== g.groupSummaryPos[l.idx]) {
                                var
                                z;
                                if (void
                                0 !== v) {
                                    for (z = 0; z < g.groupField.length && v.dataIndex !== g.groupField[z]; z++);
                                    m = g.groupField.length - z
                                }
                                for (t = 0; t < m; t++) p[t] && (r = e(d, t, g.groups, 0), f += r.join(c.separator) + c.newLine);
                                m = z
                            }
                        }
                    }), f
                }
                b._regexsep = new
                RegExp(b.separator, "g"), b._regexquot = new
                RegExp(b.quote, "g");
                var
                e, f, g, h, i, j = this,
                    k = this.addLocalData(!0),
                    l = k.length,
                    m = j.p.colModel,
                    n = m.length,
                    o = j.p.colNames,
                    p = 0,
                    q = "",
                    r = "",
                    s = "",
                    t = "",
                    u = "",
                    v = [],
                    w = [],
                    x = [],
                    y = [];
                if (a.each(m, function (c, d) {
                    void
                    0 === d.exportcol && (d.exportcol = !0), "cb" !== d.name && "rn" !== d.name || d.hidden || (w.push(c), d.hidden = !0), d.exportcol || d.hidden || (y.push(c), d.hidden = !0), !d.hidden && d.exportcol && (v.push(a.jgrid.formatCellCsv(o[c], b)), x.push(d.name))
                }), b.includeLabels && (u = v.join(b.separator) + b.newLine), b.collen = v.length, j.p.grouping) q += d(k, b);
                else for (; p < l;) {
                    for (f = k[p], g = [], h = 0, e = 0; e < n; e++) m[e].hidden || (g[h] = a.jgrid.formatCellCsv(a.jgrid.formatCell(f[m[e].name], e, f, m[e], j), b), h++);
                    q += g.join(b.separator) + b.newLine, p++
                }
                if (k = null, g = new
                Array(b.collen), b.includeCaption && j.p.caption) {
                    for (p = b.collen; --p;) g[p] = "";
                    g[0] = a.jgrid.formatCellCsv(j.p.caption, b), r += g.join(b.separator) + b.newLine
                }
                if (b.includeGroupHeader && j.p.groupHeader && j.p.groupHeader.length) {
                    var
                    z = j.p.groupHeader;
                    for (e = 0; e < z.length; e++) {
                        var
                        A = z[e].groupHeaders;
                        for (p = 0, g = [], i = 0; i < x.length; i++) {
                            for (g[p] = "", h = 0; h < A.length; h++) A[h].startColumnName === x[i] && (g[p] = a.jgrid.formatCellCsv(A[h].titleText, b));
                            p++
                        }
                        s += g.join(b.separator) + b.newLine
                    }
                }
                if (b.includeFooter && j.p.footerrow) {
                    var
                    B = a(".ui-jqgrid-ftable", this.sDiv);
                    if (B.length) {
                        var
                        C = B[0].rows[0];
                        for (e = 0, p = 0, g = []; e < C.cells.length;) {
                            var
                            D = C.cells[e],
                                E = a(D).attr("aria-describedby").slice(-3);
                            D.hidden || "_cb" === E || "_rn" === E || (g[p] = a.jgrid.formatCellCsv(a(D).text(), b), p++), e++
                        }
                        t += g.join(b.separator) + b.newLine
                    }
                }
                for (c = r + s + u + q + t, e = 0; e < w.length; e++) m[w[e]].hidden = !1;
                for (e = 0; e < y.length; e++) m[y[e]].hidden = !1
            }), b.returnAsString) return c;
            a.jgrid.saveAs(c, b.fileName, {
                type: b.mimetype
            })
        },
        exportToExcel: function (b) {
            b = a.extend(!0, {
                includeLabels: !0,
                includeGroupHeader: !0,
                includeFooter: !0,
                fileName: "jqGridExport.xlsx",
                mimetype: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                maxlength: 40,
                onBeforeExport: null,
                replaceStr: null
            }, b || {}), this.each(function () {
                function
                c(a) {
                    return a.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F-\x9F]/g, "")
                }

                function
                d(b) {
                    function
                    c(a, b, c) {
                        var
                        d, e = !1;
                        if (0 === b) e = c[a];
                        else {
                            var
                            f = c[a].idx;
                            if (0 === f) e = c[a];
                            else for (d = a; d >= 0; d--) if (c[d].idx === f - b) {
                                e = c[d];
                                break
                            }
                        }
                        return e
                    }

                    function
                    d(b, d, f, h) {
                        var
                        i, k, l = c(b, d, f),
                            n = l.cnt,
                            p = e(o.header);
                        for (k = h; k < j; k++) if (!m[k].hidden && !m[k].exportcol) {
                            var
                            q = "{0}";
                            a.each(l.summary, function () {
                                if (this.nm === m[k].name) {
                                    m[k].summaryTpl && (q = m[k].summaryTpl), "string" == typeof
                                    this.st && "avg" === this.st.toLowerCase() && (this.sd && this.vd ? this.v = this.v / this.vd : this.v && n > 0 && (this.v = this.v / n));
                                    try {
                                        this.groupCount = l.cnt, this.groupIndex = l.dataIndex, this.groupValue = l.value, i = g.formatter("", this.v, k, this)
                                    } catch (a) {
                                        i = this.v
                                    }
                                    return p[this.nm] = a.jgrid.stripHtml(a.jgrid.template(q, i)), !1
                                }
                            })
                        }
                        return p
                    }

                    function
                    e(a) {
                        for (var
                        b = {}, c = 0; c < a.length; c++) b[a[c]] = "";
                        return b
                    }
                    var
                    f = g.p.groupingView,
                        h = [],
                        i = f.groupField.length,
                        j = m.length,
                        k = 0;
                    a.each(m, function (a, b) {
                        var
                        c;
                        for (c = 0; c < i; c++) if (f.groupField[c] === b.name) {
                            h[c] = a;
                            break
                        }
                    });
                    var
                    l, n = a.makeArray(f.groupSummary);
                    n.reverse(), a.each(f.groups, function (c, j) {
                        k++;
                        try {
                            l = a.isArray(f.formatDisplayField) && a.isFunction(f.formatDisplayField[j.idx]) ? f.formatDisplayField[j.idx].call(g, j.displayValue, j.value, g.p.colModel[h[j.idx]], j.idx, f) : g.formatter("", j.displayValue, h[j.idx], j.value)
                        } catch (a) {
                            l = j.displayValue
                        }
                        var
                        m = "";
                        "string" != typeof (m = a.isFunction(f.groupText[j.idx]) ? f.groupText[j.idx].call(g, l, j.cnt, j.summary) : a.jgrid.template(f.groupText[j.idx], l, j.cnt, j.summary)) && "number" != typeof
                        m && (m = l);
                        var
                        p;
                        if (p = "header" === f.groupSummaryPos[j.idx] ? d(c, 0, f.groups, 0) : e(o.header), p[Object.keys(p)[0]] = a.jgrid.stripHtml(new
                        Array(5 * j.idx).join(" ") + m), s(p, !0), i - 1 === j.idx) {
                            var
                            q, r, t = f.groups[c + 1],
                                u = 0,
                                v = j.startRow,
                                w = void
                                0 !== t ? t.startRow : f.groups[c].startRow + f.groups[c].cnt;
                            for (q = v; q < w && b[q - u]; q++) {
                                var
                                x = b[q - u];
                                s(x, !1)
                            }
                            if ("header" !== f.groupSummaryPos[j.idx]) {
                                var
                                y;
                                if (void
                                0 !== t) {
                                    for (y = 0; y < f.groupField.length && t.dataIndex !== f.groupField[y]; y++);
                                    k = f.groupField.length - y
                                }
                                for (r = 0; r < k; r++) n[r] && (p = d(c, r, f.groups, 0), s(p, !0));
                                k = y
                            }
                        }
                    })
                }
                var
                e, f, g = this,
                    h = a.jgrid.excelStrings,
                    i = 0,
                    j = a.parseXML(h["xl/worksheets/sheet1.xml"]),
                    k = j.getElementsByTagName("sheetData")[0],
                    l = {
                        _rels: {
                            ".rels": a.parseXML(h["_rels/.rels"])
                        },
                        xl: {
                            _rels: {
                                "workbook.xml.rels": a.parseXML(h["xl/_rels/workbook.xml.rels"])
                            },
                            "workbook.xml": a.parseXML(h["xl/workbook.xml"]),
                            "styles.xml": a.parseXML(h["xl/styles.xml"]),
                            worksheets: {
                                "sheet1.xml": j
                            }
                        },
                        "[Content_Types].xml": a.parseXML(h["[Content_Types].xml"])
                    }, m = g.p.colModel,
                    n = 0,
                    o = {
                        body: g.addLocalData(!0),
                        header: [],
                        footer: [],
                        width: [],
                        map: []
                    };
                for (e = 0, f = m.length; e < f; e++) void
                0 === m[e].exportcol && (m[e].exportcol = !0), !m[e].hidden && "cb" !== m[e].name && "rn" !== m[e].name && m[e].exportcol && (o.header[n] = m[e].name, o.width[n] = 5, o.map[n] = e, n++);
                var
                p, q, r = a.isFunction(b.replaceStr) ? b.replaceStr : c,
                    s = function (c, d) {
                        p = i + 1, q = a.jgrid.makeNode(j, "row", {
                            attr: {
                                r: p
                            }
                        });
                        for (var
                        e = 0; e < o.header.length; e++) {
                            var
                            f, h = a.jgrid.excelCellPos(e) + "" + p,
                                l = a.isArray(c) && d ? g.p.colNames[o.map[e]] : c[o.header[e]];
                            if (null == l && (l = ""), d || (l = "" !== l ? a.jgrid.formatCell(l, o.map[e], c, m[o.map[e]], g) : l), o.width[e] = Math.max(o.width[e], Math.min(parseInt(l.length, 10), b.maxlength)), "number" == typeof
                            l || l.match && a.trim(l).match(/^-?\d+(\.\d+)?$/) && !a.trim(l).match(/^0\d+/)) f = a.jgrid.makeNode(j, "c", {
                                attr: {
                                    t: "n",
                                    r: h
                                },
                                children: [a.jgrid.makeNode(j, "v", {
                                    text: l
                                })]
                            });
                            else {
                                var
                                n = l.replace ? r(l) : l;
                                f = a.jgrid.makeNode(j, "c", {
                                    attr: {
                                        t: "inlineStr",
                                        r: h
                                    },
                                    children: {
                                        row: a.jgrid.makeNode(j, "is", {
                                            children: {
                                                row: a.jgrid.makeNode(j, "t", {
                                                    text: n
                                                })
                                            }
                                        })
                                    }
                                })
                            }
                            q.appendChild(f)
                        }
                        k.appendChild(q), i++
                    };
                if (a("sheets sheet", l.xl["workbook.xml"]).attr("name", b.sheetName), b.includeGroupHeader && g.p.groupHeader && g.p.groupHeader.length) {
                    var
                    t, u, v = g.p.groupHeader,
                        w = [],
                        x = 0;
                    for (u = 0; u < v.length; u++) {
                        var
                        y = v[u].groupHeaders,
                            z = {};
                        for (x++, e = 0, e = 0; e < o.header.length; e++) {
                            t = o.header[e], z[t] = "";
                            for (var
                            A = 0; A < y.length; A++) if (y[A].startColumnName === t) {
                                z[t] = y[A].titleText;
                                var
                                B = a.jgrid.excelCellPos(e) + x,
                                    C = a.jgrid.excelCellPos(e + y[A].numberOfColumns - 1) + x;
                                w.push({
                                    ref: B + ":" + C
                                })
                            }
                        }
                        s(z, !0)
                    }
                    a("row c", j).attr("s", "2");
                    var
                    D = a.jgrid.makeNode(j, "mergeCells", {
                        attr: {
                            count: w.length
                        }
                    });
                    for (a("worksheet", j).append(D), n = 0; n < w.length; n++) D.appendChild(a.jgrid.makeNode(j, "mergeCell", {
                        attr: w[n]
                    }))
                }
                if (b.includeLabels && (s(o.header, !0), a("row:last c", j).attr("s", "2")), g.p.grouping) d(o.body);
                else for (var
                E = 0, F = o.body.length; E < F; E++) s(o.body[E], !1);
                if (b.includeFooter || g.p.footerrow) {
                    o.footer = a(g).jqGrid("footerData", "get");
                    for (n in o.footer) o.footer.hasOwnProperty(n) && (o.footer[n] = a.jgrid.stripHtml(o.footer[n]));
                    s(o.footer, !0), a("row:last c", j).attr("s", "2")
                }
                var
                G = a.jgrid.makeNode(j, "cols");
                for (a("worksheet", j).prepend(G), n = 0, f = o.width.length; n < f; n++) G.appendChild(a.jgrid.makeNode(j, "col", {
                    attr: {
                        min: n + 1,
                        max: n + 1,
                        width: o.width[n],
                        customWidth: 1
                    }
                }));
                a.isFunction(b.onBeforeExport) && b.onBeforeExport(l), o = null;
                try {
                    var
                    H = new
                    JSZip,
                        I = {
                            type: "blob",
                            mimeType: b.mimetype
                        };
                    a.jgrid.xmlToZip(H, l), H.generateAsync ? H.generateAsync(I).then(function (c) {
                        a.jgrid.saveAs(c, b.fileName, {
                            type: b.mimetype
                        })
                    }) : a.jgrid.saveAs(H.generate(I), b.fileName, {
                        type: b.mimetype
                    })
                } catch (a) {
                    throw a
                }
            })
        },
        exportToPdf: function (b) {
            return b = a.extend(!0, {
                title: null,
                orientation: "portrait",
                pageSize: "A4",
                description: null,
                onBeforeExport: null,
                download: "download",
                includeLabels: !0,
                includeGroupHeader: !0,
                includeFooter: !0,
                fileName: "jqGridExport.pdf",
                mimetype: "application/pdf"
            }, b || {}), this.each(function () {
                function
                c(b) {
                    function
                    c(b, c) {
                        for (var
                        d = 0, e = [], f = 0; f < m.length; f++) k = {
                            text: null == b[m[f]] ? "" : c ? a.jgrid.formatCell(b[m[f]] + "", o[d], l[n], q[o[d]], h) : b[m[f]],
                            alignment: r[f],
                            style: "tableBody"
                        }, e.push(k), d++;
                        return e
                    }

                    function
                    d(a, b, c) {
                        var
                        d, e = !1;
                        if (0 === b) e = c[a];
                        else {
                            var
                            f = c[a].idx;
                            if (0 === f) e = c[a];
                            else for (d = a; d >= 0; d--) if (c[d].idx === f - b) {
                                e = c[d];
                                break
                            }
                        }
                        return e
                    }

                    function
                    e(b, c, e, g) {
                        var
                        i, j, k = d(b, c, e),
                            l = k.cnt,
                            n = f(m);
                        for (j = g; j < s; j++) if (!q[j].hidden && q[j].exportcol) {
                            var
                            o = "{0}";
                            a.each(k.summary, function () {
                                if (this.nm === q[j].name) {
                                    q[j].summaryTpl && (o = q[j].summaryTpl), "string" == typeof
                                    this.st && "avg" === this.st.toLowerCase() && (this.sd && this.vd ? this.v = this.v / this.vd : this.v && l > 0 && (this.v = this.v / l));
                                    try {
                                        this.groupCount = k.cnt, this.groupIndex = k.dataIndex, this.groupValue = k.value, i = h.formatter("", this.v, j, this)
                                    } catch (a) {
                                        i = this.v
                                    }
                                    return n[this.nm] = a.jgrid.stripHtml(a.jgrid.template(o, i)), !1
                                }
                            })
                        }
                        return n
                    }

                    function
                    f(a) {
                        for (var
                        b = {}, c = 0; c < a.length; c++) b[a[c]] = "";
                        return b
                    }
                    var
                    g = h.p.groupingView,
                        j = [],
                        p = g.groupField.length,
                        q = h.p.colModel,
                        s = q.length,
                        t = 0;
                    a.each(q, function (a, b) {
                        var
                        c;
                        for (c = 0; c < p; c++) if (g.groupField[c] === b.name) {
                            j[c] = a;
                            break
                        }
                    });
                    var
                    u, v = a.makeArray(g.groupSummary);
                    v.reverse(), a.each(g.groups, function (d, k) {
                        t++;
                        try {
                            u = a.isArray(g.formatDisplayField) && a.isFunction(g.formatDisplayField[k.idx]) ? g.formatDisplayField[k.idx].call(h, k.displayValue, k.value, h.p.colModel[j[k.idx]], k.idx, g) : h.formatter("", k.displayValue, j[k.idx], k.value)
                        } catch (a) {
                            u = k.displayValue
                        }
                        var
                        l = "";
                        "string" != typeof (l = a.isFunction(g.groupText[k.idx]) ? g.groupText[k.idx].call(h, u, k.cnt, k.summary) : a.jgrid.template(g.groupText[k.idx], u, k.cnt, k.summary)) && "number" != typeof
                        l && (l = u);
                        var
                        n;
                        if (n = "header" === g.groupSummaryPos[k.idx] ? e(d, 0, g.groups, 0) : f(m), n[Object.keys(n)[0]] = a.jgrid.stripHtml(new
                        Array(5 * k.idx).join(" ") + l), i.push(c(n, !1)), p - 1 === k.idx) {
                            var
                            o, q, r = g.groups[d + 1],
                                s = 0,
                                w = k.startRow,
                                x = void
                                0 !== r ? r.startRow : g.groups[d].startRow + g.groups[d].cnt;
                            for (o = w; o < x && b[o - s]; o++) {
                                var
                                y = b[o - s];
                                i.push(c(y, !0))
                            }
                            if ("header" !== g.groupSummaryPos[k.idx]) {
                                var
                                z;
                                if (void
                                0 !== r) {
                                    for (z = 0; z < g.groupField.length && r.dataIndex !== g.groupField[z]; z++);
                                    t = g.groupField.length - z
                                }
                                for (q = 0; q < t; q++) v[q] && (n = e(d, q, g.groups, 0), i.push(c(n, !1)));
                                t = z
                            }
                        }
                    })
                }
                var
                d, e, f, g, h = this,
                    i = [],
                    j = h.p.colModel,
                    k = {}, l = h.addLocalData(!0),
                    m = [],
                    n = 0,
                    o = [],
                    p = [],
                    q = [],
                    r = {};
                for (d = 0, e = j.length; d < e; d++) void
                0 === j[d].exportcol && (j[d].exportcol = !0), !j[d].hidden && "cb" !== j[d].name && "rn" !== j[d].name && j[d].exportcol && (k = {
                    text: h.p.colNames[d],
                    style: "tableHeader"
                }, p.push(k), m[n] = j[d].name, o[n] = d, q.push(j[d].width), r[j[d].name] = j[d].align || "left", n++);
                var
                s;
                if (b.includeGroupHeader && h.p.groupHeader && h.p.groupHeader.length) for (s = h.p.groupHeader, n = 0; n < s.length; n++) {
                    var
                    t = [],
                        u = s[n].groupHeaders;
                    for (f = 0; f < m.length; f++) {
                        for (k = {
                            text: "",
                            style: "tableHeader"
                        }, g = 0; g < u.length; g++) u[g].startColumnName === m[f] && (k = {
                            text: u[g].titleText,
                            colSpan: u[g].numberOfColumns,
                            style: "tableHeader"
                        });
                        t.push(k), d++
                    }
                    i.push(t)
                }
                if (b.includeLabels && i.push(p), h.p.grouping) c(l);
                else {
                    var
                    v;
                    for (n = 0, e = l.length; n < e; n++) {
                        for (g = 0, p = [], v = l[n], f = 0; f < m.length; f++) k = {
                            text: null == v[m[f]] ? "" : a.jgrid.formatCell(v[m[f]] + "", o[g], l[n], j[o[g]], h),
                            alignment: r[m[f]],
                            style: "tableBody"
                        }, p.push(k), g++;
                        i.push(p)
                    }
                }
                if (b.includeFooter && h.p.footerrow) {
                    var
                    w = a(h).jqGrid("footerData", "get");
                    for (p = [], f = 0; f < m.length; f++) k = {
                        text: a.jgrid.stripHtml(w[m[f]]),
                        style: "tableFooter",
                        alignment: r[m[f]]
                    }, p.push(k);
                    i.push(p)
                }
                var
                x = {
                    pageSize: b.pageSize,
                    pageOrientation: b.orientation,
                    content: [{
                        style: "tableExample",
                        widths: q,
                        table: {
                            headerRows: null != s ? 0 : 1,
                            body: i
                        }
                    }],
                    styles: {
                        tableHeader: {
                            bold: !0,
                            fontSize: 11,
                            color: "#2e6e9e",
                            fillColor: "#dfeffc",
                            alignment: "center"
                        },
                        tableBody: {
                            fontSize: 10
                        },
                        tableFooter: {
                            bold: !0,
                            fontSize: 11,
                            color: "#2e6e9e",
                            fillColor: "#dfeffc"
                        },
                        title: {
                            alignment: "center",
                            fontSize: 15
                        },
                        description: {}
                    },
                    defaultStyle: {
                        fontSize: 10
                    }
                };
                b.description && x.content.unshift({
                    text: b.description,
                    style: "description",
                    margin: [0, 0, 0, 12]
                }), b.title && x.content.unshift({
                    text: b.title,
                    style: "title",
                    margin: [0, 0, 0, 12]
                }), a.isFunction(b.onBeforeExport) && b.onBeforeExport.call(h, x);
                try {
                    var
                    y = pdfMake.createPdf(x);
                    "open" === b.download ? y.open() : y.getBuffer(function (c) {
                        a.jgrid.saveAs(c, b.fileName, {
                            type: b.mimetype
                        })
                    })
                } catch (a) {
                    throw a
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery"], a) : a()
}(function () {
    "use strict";
    $.extend($.jgrid, {
        stringify: function (a) {
            return JSON.stringify(a, function (a, b) {
                return "function" == typeof
                b ? b.toString() : b
            })
        },
        parseFunc: function (str) {
            return JSON.parse(str, function (key, value) {
                if ("string" == typeof
                value && -1 !== value.indexOf("function")) {
                    var
                    sv = value.split(" ");
                    return "function" === sv[0].trim() && "}" === value.trim().slice(-1) ? eval("(" + value + ")") : value
                }
                return value
            })
        },
        encode: function (a) {
            return String(a).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;")
        },
        jsonToXML: function (a, b) {
            var
            c = $.extend({
                xmlDecl: '<?xml version="1.0" encoding="UTF-8" ?>\n',
                attr_prefix: "-",
                encode: !0
            }, b || {}),
                d = this,
                e = function (a, b) {
                    return "#text" === a ? c.encode ? d.encode(b) : b : "function" == typeof
                    b ? "<" + a + "><![CDATA[" + b + "]]></" + a + ">\n" : "" === b ? "<" + a + ">__EMPTY_STRING_</" + a + ">\n" : "<" + a + ">" + (c.encode ? d.encode(b) : b) + "</" + a + ">\n"
                }, f = function (a, b) {
                    for (var
                    c = [], d = 0; d < b.length; d++) {
                        var
                        h = b[d];
                        void
                        0 === h || null == h ? c[c.length] = "<" + a + " />" : "object" == typeof
                        h && h.constructor == Array ? c[c.length] = f(a, h) : c[c.length] = "object" == typeof
                        h ? g(a, h) : e(a, h)
                    }
                    return c.length || (c[0] = "<" + a + ">__EMPTY_ARRAY_</" + a + ">\n"), c.join("")
                }, g = function (a, b) {
                    var
                    h = [],
                        i = [];
                    for (var
                    j in b) if (b.hasOwnProperty(j)) {
                        var
                        k = b[j];
                        j.charAt(0) !== c.attr_prefix ? null == k ? h[h.length] = "<" + j + " />" : "object" == typeof
                        k && k.constructor === Array ? h[h.length] = f(j, k) : h[h.length] = "object" == typeof
                        k ? g(j, k) : e(j, k) : i[i.length] = " " + j.substring(1) + '="' + (c.encode ? d.encode(k) : k) + '"'
                    }
                    var
                    l = i.join(""),
                        m = h.join("");
                    return null == a || (m = h.length > 0 ? m.match(/\n/) ? "<" + a + l + ">\n" + m + "</" + a + ">\n" : "<" + a + l + ">" + m + "</" + a + ">\n" : "<" + a + l + " />\n"), m
                }, h = g(null, a);
            return c.xmlDecl + h
        },
        xmlToJSON: function (root, options) {
            var
            o = $.extend({
                force_array: [],
                attr_prefix: "-"
            }, options || {});
            if (root) {
                var
                __force_array = {};
                if (o.force_array) for (var
                i = 0; i < o.force_array.length; i++) __force_array[o.force_array[i]] = 1;
                "string" == typeof
                root && (root = $.parseXML(root)), root.documentElement && (root = root.documentElement);
                var
                addNode = function (hash, key, cnts, val) {
                    if ("string" == typeof
                    val) if (-1 !== val.indexOf("function")) val = eval("(" + val + ")");
                    else switch (val) {
                        case "__EMPTY_ARRAY_":
                            val = [];
                            break;
                        case "__EMPTY_STRING_":
                            val = "";
                            break;
                        case "false":
                            val = !1;
                            break;
                        case "true":
                            val = !0
                    }
                    __force_array[key] ? (1 === cnts && (hash[key] = []), hash[key][hash[key].length] = val) : 1 === cnts ? hash[key] = val : 2 === cnts ? hash[key] = [hash[key], val] : hash[key][hash[key].length] = val
                }, parseElement = function (a) {
                    if (7 !== a.nodeType) {
                        if (3 === a.nodeType || 4 === a.nodeType) {
                            if (null == a.nodeValue.match(/[^\x00-\x20]/)) return;
                            return a.nodeValue
                        }
                        var
                        b, c, d, e, f = {};
                        if (a.attributes && a.attributes.length) for (b = {}, c = 0; c < a.attributes.length; c++) "string" == typeof (d = a.attributes[c].nodeName) && (e = a.attributes[c].nodeValue) && (d = o.attr_prefix + d, void
                        0 === f[d] && (f[d] = 0), f[d]++, addNode(b, d, f[d], e));
                        if (a.childNodes && a.childNodes.length) {
                            var
                            g = !0;
                            for (b && (g = !1), c = 0; c < a.childNodes.length && g; c++) {
                                var
                                h = a.childNodes[c].nodeType;
                                3 !== h && 4 !== h && (g = !1)
                            }
                            if (g) for (b || (b = ""), c = 0; c < a.childNodes.length; c++) b += a.childNodes[c].nodeValue;
                            else for (b || (b = {}), c = 0; c < a.childNodes.length; c++) "string" == typeof (d = a.childNodes[c].nodeName) && (e = parseElement(a.childNodes[c])) && (void
                            0 === f[d] && (f[d] = 0), f[d]++, addNode(b, d, f[d], e))
                        }
                        return b
                    }
                }, json = parseElement(root);
                if (__force_array[root.nodeName] && (json = [json]), 11 !== root.nodeType) {
                    var
                    tmp = {};
                    tmp[root.nodeName] = json, json = tmp
                }
                return json
            }
        },
        saveAs: function (a, b, c) {
            c = $.extend(!0, {
                type: "plain/text;charset=utf-8"
            }, c || {});
            var
            d, e, f = [];
            b = null == b || "" === b ? "jqGridFile.txt" : b, $.isArray(a) ? f = a : f[0] = a;
            try {
                d = new
                File(f, b, c)
            } catch (a) {
                d = new
                Blob(f, c)
            }
            if (window.navigator && window.navigator.msSaveOrOpenBlob) window.navigator.msSaveOrOpenBlob(d, b);
            else {
                e = URL.createObjectURL(d);
                var
                g = document.createElement("a");
                g.href = e, g.download = b, document.body.appendChild(g), g.click(), setTimeout(function () {
                    document.body.removeChild(g), window.URL.revokeObjectURL(e)
                }, 0)
            }
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery", "./grid.base", "jquery-ui/dialog", "jquery-ui/draggable", "jquery-ui/droppable", "jquery-ui/resizable", "jquery-ui/sortable", "./addons/ui.multiselect"], a) : a(jQuery)
}(function ($) {
    "use strict";
    if ($.jgrid.msie() && 8 === $.jgrid.msiever() && ($.expr[":"].hidden = function (a) {
        return 0 === a.offsetWidth || 0 === a.offsetHeight || "none" === a.style.display
    }), $.jgrid._multiselect = !1, $.ui && $.ui.multiselect) {
        if ($.ui.multiselect.prototype._setSelected) {
            var
            setSelected = $.ui.multiselect.prototype._setSelected;
            $.ui.multiselect.prototype._setSelected = function (a, b) {
                var
                c = setSelected.call(this, a, b);
                if (b && this.selectedList) {
                    var
                    d = this.element;
                    this.selectedList.find("li").each(function () {
                        $(this).data("optionLink") && $(this).data("optionLink").remove().appendTo(d)
                    })
                }
                return c
            }
        }
        $.ui.multiselect.prototype.destroy && ($.ui.multiselect.prototype.destroy = function () {
            this.element.show(), this.container.remove(), void
            0 === $.Widget ? $.widget.prototype.destroy.apply(this, arguments) : $.Widget.prototype.destroy.apply(this, arguments)
        }), $.jgrid._multiselect = !0
    }
    $.jgrid.extend({
        sortableColumns: function (a) {
            return this.each(function () {
                function
                b() {
                    d.p.disableClick = !0
                }

                function
                c() {
                    setTimeout(function () {
                        d.p.disableClick = !1
                    }, 50)
                }
                var
                d = this,
                    e = $.jgrid.jqID(d.p.id),
                    f = {
                        tolerance: "pointer",
                        axis: "x",
                        scrollSensitivity: "1",
                        items: ">th:not(:has(#jqgh_" + e + "_cb,#jqgh_" + e + "_rn,#jqgh_" + e + "_subgrid),:hidden)",
                        placeholder: {
                            element: function (a) {
                                return $(document.createElement(a[0].nodeName)).addClass(a[0].className + " ui-sortable-placeholder ui-state-highlight").removeClass("ui-sortable-helper")[0]
                            },
                            update: function (a, b) {
                                b.height(a.currentItem.innerHeight() - parseInt(a.currentItem.css("paddingTop") || 0, 10) - parseInt(a.currentItem.css("paddingBottom") || 0, 10)), b.width(a.currentItem.innerWidth() - parseInt(a.currentItem.css("paddingLeft") || 0, 10) - parseInt(a.currentItem.css("paddingRight") || 0, 10))
                            }
                        },
                        update: function (a, b) {
                            var
                            c = $(b.item).parent(),
                                e = $(">th", c),
                                f = d.p.colModel,
                                g = {}, h = d.p.id + "_";
                            $.each(f, function (a) {
                                g[this.name] = a
                            });
                            var
                            i = [];
                            e.each(function () {
                                var
                                a = $(">div", this).get(0).id.replace(/^jqgh_/, "").replace(h, "");
                                g.hasOwnProperty(a) && i.push(g[a])
                            }), $(d).jqGrid("remapColumns", i, !0, !0), $.isFunction(d.p.sortable.update) && d.p.sortable.update(i)
                        }
                    };
                if (d.p.sortable.options ? $.extend(f, d.p.sortable.options) : $.isFunction(d.p.sortable) && (d.p.sortable = {
                    update: d.p.sortable
                }), f.start) {
                    var
                    g = f.start;
                    f.start = function (a, c) {
                        b(), g.call(this, a, c)
                    }
                } else f.start = b;
                if (f.stop) {
                    var
                    h = f.stop;
                    f.stop = function (a, b) {
                        c(), h.call(this, a, b)
                    }
                } else f.stop = c;
                d.p.sortable.exclude && (f.items += ":not(" + d.p.sortable.exclude + ")");
                var
                i = a.sortable(f),
                    j = i.data("sortable") || i.data("uiSortable");
                null != j && (j.data("sortable").floating = !0)
            })
        },
        columnChooser: function (a) {
            function
            b(a, b, c) {
                var
                d, e;
                return b >= 0 ? (d = a.slice(), e = d.splice(b, Math.max(a.length - b, b)), b > a.length && (b = a.length), d[b] = c, d.concat(e)) : a
            }

            function
            c(a, b) {
                a && ("string" == typeof
                a ? $.fn[a] && $.fn[a].apply(b, $.makeArray(arguments).slice(2)) : $.isFunction(a) && a.apply(b, $.makeArray(arguments).slice(2)))
            }

            function
            d() {
                var
                a = q(f),
                    b = a.container.closest(".ui-dialog-content");
                b.length > 0 && "object" == typeof
                b[0].style ? b[0].style.width = "" : b.css("width", ""), a.selectedList.height(Math.max(a.selectedContainer.height() - a.selectedActions.outerHeight() - 1, 1)), a.availableList.height(Math.max(a.availableContainer.height() - a.availableActions.outerHeight() - 1, 1))
            }
            var
            e, f, g, h, i, j, k, l = this,
                m = {}, n = [],
                o = l.jqGrid("getGridParam", "colModel"),
                p = l.jqGrid("getGridParam", "colNames"),
                q = function (a) {
                    return $.ui.multiselect.prototype && a.data($.ui.multiselect.prototype.widgetFullName || $.ui.multiselect.prototype.widgetName) || a.data("ui-multiselect") || a.data("multiselect")
                }, r = $.jgrid.getRegional(this[0], "col");
            if (!$("#colchooser_" + $.jgrid.jqID(l[0].p.id)).length) {
                if (e = $('<div id="colchooser_' + l[0].p.id + '" style="position:relative;overflow:hidden"><div><select multiple="multiple"></select></div></div>'), f = $("select", e), a = $.extend({
                    width: 400,
                    height: 240,
                    classname: null,
                    done: function (a) {
                        a && l.jqGrid("remapColumns", a, !0)
                    },
                    msel: "multiselect",
                    dlog: "dialog",
                    dialog_opts: {
                        minWidth: 470,
                        dialogClass: "ui-jqdialog"
                    },
                    dlog_opts: function (a) {
                        var
                        b = {};
                        return b[a.bSubmit] = function () {
                            a.apply_perm(), a.cleanup(!1)
                        }, b[a.bCancel] = function () {
                            a.cleanup(!0)
                        }, $.extend(!0, {
                            buttons: b,
                            close: function () {
                                a.cleanup(!0)
                            },
                            modal: a.modal || !1,
                            resizable: a.resizable || !0,
                            width: a.width + 70,
                            resize: d
                        }, a.dialog_opts || {})
                    },
                    apply_perm: function () {
                        var
                        c = [];
                        $("option", f).each(function () {
                            $(this).is(":selected") ? l.jqGrid("showCol", o[this.value].name) : l.jqGrid("hideCol", o[this.value].name)
                        }), $("option[selected]", f).each(function () {
                            c.push(parseInt(this.value, 10))
                        }), $.each(c, function () {
                            delete
                            m[o[parseInt(this, 10)].name]
                        }), $.each(m, function () {
                            var
                            a = parseInt(this, 10);
                            c = b(c, a, a)
                        }), a.done && a.done.call(l, c), l.jqGrid("setGridWidth", l[0].p.width, l[0].p.shrinkToFit)
                    },
                    cleanup: function (b) {
                        c(a.dlog, e, "destroy"), c(a.msel, f, "destroy"), e.remove(), b && a.done && a.done.call(l)
                    },
                    msel_opts: {}
                }, r, a || {}), $.ui && $.ui.multiselect && $.ui.multiselect.defaults) {
                    if (!$.jgrid._multiselect) return void
                    alert("Multiselect plugin loaded after jqGrid. Please load the plugin before the jqGrid!");
                    a.msel_opts = $.extend($.ui.multiselect.defaults, a.msel_opts)
                }
                a.caption && e.attr("title", a.caption), a.classname && (e.addClass(a.classname), f.addClass(a.classname)), a.width && ($(">div", e).css({
                    width: a.width,
                    margin: "0 auto"
                }), f.css("width", a.width)), a.height && ($(">div", e).css("height", a.height), f.css("height", a.height - 10)), f.empty(), $.each(o, function (a) {
                    if (m[this.name] = a, this.hidedlg) return void(this.hidden || n.push(a));
                    f.append("<option value='" + a + "' " + (this.hidden ? "" : "selected='selected'") + ">" + $.jgrid.stripHtml(p[a]) + "</option>")
                }), g = $.isFunction(a.dlog_opts) ? a.dlog_opts.call(l, a) : a.dlog_opts, c(a.dlog, e, g), h = $.isFunction(a.msel_opts) ? a.msel_opts.call(l, a) : a.msel_opts, c(a.msel, f, h), i = $("#colchooser_" + $.jgrid.jqID(l[0].p.id)), i.css({
                    margin: "auto"
                }), i.find(">div").css({
                    width: "100%",
                    height: "100%",
                    margin: "auto"
                }), j = q(f), j.container.css({
                    width: "100%",
                    height: "100%",
                    margin: "auto"
                }), j.selectedContainer.css({
                    width: 100 * j.options.dividerLocation + "%",
                    height: "100%",
                    margin: "auto",
                    boxSizing: "border-box"
                }), j.availableContainer.css({
                    width: 100 - 100 * j.options.dividerLocation + "%",
                    height: "100%",
                    margin: "auto",
                    boxSizing: "border-box"
                }), j.selectedList.css("height", "auto"), j.availableList.css("height", "auto"), k = Math.max(j.selectedList.height(), j.availableList.height()), k = Math.min(k, $(window).height()), j.selectedList.css("height", k), j.availableList.css("height", k), d()
            }
        },
        sortableRows: function (a) {
            return this.each(function () {
                var
                b = this;
                b.grid && (b.p.treeGrid || $.fn.sortable && (a = $.extend({
                    cursor: "move",
                    axis: "y",
                    items: " > .jqgrow"
                }, a || {}), a.start && $.isFunction(a.start) ? (a._start_ = a.start, delete
                a.start) : a._start_ = !1, a.update && $.isFunction(a.update) ? (a._update_ = a.update, delete
                a.update) : a._update_ = !1, a.start = function (c, d) {
                    if ($(d.item).css("border-width", "0"), $("td", d.item).each(function (a) {
                        this.style.width = b.grid.cols[a].style.width
                    }), b.p.subGrid) {
                        var
                        e = $(d.item).attr("id");
                        try {
                            $(b).jqGrid("collapseSubGridRow", e)
                        } catch (a) {}
                    }
                    a._start_ && a._start_.apply(this, [c, d])
                }, a.update = function (c, d) {
                    $(d.item).css("border-width", ""), !0 === b.p.rownumbers && $("td.jqgrid-rownum", b.rows).each(function (a) {
                        $(this).html(a + 1 + (parseInt(b.p.page, 10) - 1) * parseInt(b.p.rowNum, 10))
                    }), a._update_ && a._update_.apply(this, [c, d])
                }, $("tbody:first", b).sortable(a), $("tbody:first > .jqgrow", b).disableSelection()))
            })
        },
        gridDnD: function (a) {
            return this.each(function () {
                function
                b() {
                    var
                    a = $.data(e, "dnd");
                    $("tr.jqgrow:not(.ui-draggable)", e).draggable($.isFunction(a.drag) ? a.drag.call($(e), a) : a.drag)
                }
                var
                c, d, e = this;
                if (e.grid && !e.p.treeGrid && $.fn.draggable && $.fn.droppable) {
                    if (void
                    0 === $("#jqgrid_dnd")[0] && $("body").append("<table id='jqgrid_dnd' class='ui-jqgrid-dnd'></table>"), "string" == typeof
                    a && "updateDnD" === a && !0 === e.p.jqgdnd) return void
                    b();
                    var
                    f;
                    if (a = $.extend({
                        drag: function (a) {
                            return $.extend({
                                start: function (b, c) {
                                    var
                                    d, f;
                                    if (e.p.subGrid) {
                                        f = $(c.helper).attr("id");
                                        try {
                                            $(e).jqGrid("collapseSubGridRow", f)
                                        } catch (a) {}
                                    }
                                    for (d = 0; d < $.data(e, "dnd").connectWith.length; d++) 0 === $($.data(e, "dnd").connectWith[d]).jqGrid("getGridParam", "reccount") && $($.data(e, "dnd").connectWith[d]).jqGrid("addRowData", "jqg_empty_row", {});
                                    c.helper.addClass("ui-state-highlight"), $("td", c.helper).each(function (a) {
                                        this.style.width = e.grid.headers[a].width + "px"
                                    }), a.onstart && $.isFunction(a.onstart) && a.onstart.call($(e), b, c)
                                },
                                stop: function (b, c) {
                                    var
                                    d, f;
                                    for (c.helper.dropped && !a.dragcopy && (f = $(c.helper).attr("id"), void
                                    0 === f && (f = $(this).attr("id")), $(e).jqGrid("delRowData", f)), d = 0; d < $.data(e, "dnd").connectWith.length; d++) $($.data(e, "dnd").connectWith[d]).jqGrid("delRowData", "jqg_empty_row");
                                    a.onstop && $.isFunction(a.onstop) && a.onstop.call($(e), b, c)
                                }
                            }, a.drag_opts || {})
                        },
                        drop: function (a) {
                            return $.extend({
                                accept: function (a) {
                                    if (!$(a).hasClass("jqgrow")) return a;
                                    if (f = $(a).closest("table.ui-jqgrid-btable"), f.length > 0 && void
                                    0 !== $.data(f[0], "dnd")) {
                                        var
                                        b = $.data(f[0], "dnd").connectWith;
                                        return -1 !== $.inArray("#" + $.jgrid.jqID(this.id), b)
                                    }
                                    return !1
                                },
                                drop: function (b, c) {
                                    if ($(c.draggable).hasClass("jqgrow")) {
                                        var
                                        d = $(c.draggable).attr("id"),
                                            e = c.draggable.parent().parent().jqGrid("getRowData", d);
                                        if (!a.dropbyname) {
                                            var
                                            g, h, i = 0,
                                                j = {}, k = $("#" + $.jgrid.jqID(this.id)).jqGrid("getGridParam", "colModel");
                                            try {
                                                for (h in e) e.hasOwnProperty(h) && (g = k[i].name, "cb" !== g && "rn" !== g && "subgrid" !== g && e.hasOwnProperty(h) && k[i] && (j[g] = e[h]), i++);
                                                e = j
                                            } catch (a) {}
                                        }
                                        if (c.helper.dropped = !0, $.data(f[0], "dnd").beforedrop && $.isFunction($.data(f[0], "dnd").beforedrop)) {
                                            var
                                            l = $.data(f[0], "dnd").beforedrop.call(this, b, c, e, $(f[0]), $(this));
                                            void
                                            0 !== l && null !== l && "object" == typeof
                                            l && (e = l)
                                        }
                                        if (c.helper.dropped) {
                                            var
                                            m;
                                            a.autoid && ($.isFunction(a.autoid) ? m = a.autoid.call(this, e) : (m = Math.ceil(1e3 * Math.random()), m = a.autoidprefix + m)), $("#" + $.jgrid.jqID(this.id)).jqGrid("addRowData", m, e, a.droppos)
                                        }
                                        a.ondrop && $.isFunction(a.ondrop) && a.ondrop.call(this, b, c, e)
                                    }
                                }
                            }, a.drop_opts || {})
                        },
                        onstart: null,
                        onstop: null,
                        beforedrop: null,
                        ondrop: null,
                        drop_opts: {
                            activeClass: "ui-state-active",
                            hoverClass: "ui-state-hover"
                        },
                        drag_opts: {
                            revert: "invalid",
                            helper: "clone",
                            cursor: "move",
                            appendTo: "#jqgrid_dnd",
                            zIndex: 5e3
                        },
                        dragcopy: !1,
                        dropbyname: !1,
                        droppos: "first",
                        autoid: !0,
                        autoidprefix: "dnd_"
                    }, a || {}), a.connectWith) for (a.connectWith = a.connectWith.split(","), a.connectWith = $.map(a.connectWith, function (a) {
                        return $.trim(a)
                    }), $.data(e, "dnd", a), 0 === e.p.reccount || e.p.jqgdnd || b(), e.p.jqgdnd = !0, c = 0; c < a.connectWith.length; c++) d = a.connectWith[c], $(d).droppable($.isFunction(a.drop) ? a.drop.call($(e), a) : a.drop)
                }
            })
        },
        gridResize: function (opts) {
            return this.each(function () {
                var
                $t = this,
                    gID = $.jgrid.jqID($t.p.id),
                    req;
                if ($t.grid && $.fn.resizable) {
                    if (opts = $.extend({}, opts || {}), opts.alsoResize ? (opts._alsoResize_ = opts.alsoResize, delete
                    opts.alsoResize) : opts._alsoResize_ = !1, opts.stop && $.isFunction(opts.stop) ? (opts._stop_ = opts.stop, delete
                    opts.stop) : opts._stop_ = !1, opts.stop = function (a, b) {
                        $($t).jqGrid("setGridParam", {
                            height: $("#gview_" + gID + " .ui-jqgrid-bdiv").height()
                        }), $($t).jqGrid("setGridWidth", b.size.width, opts.shrinkToFit), opts._stop_ && opts._stop_.call($t, a, b), $t.p.caption && $("#gbox_" + gID).css({
                            height: "auto"
                        }), $t.p.frozenColumns && (req && clearTimeout(req), req = setTimeout(function () {
                            req && clearTimeout(req), $("#" + gID).jqGrid("destroyFrozenColumns"), $("#" + gID).jqGrid("setFrozenColumns")
                        }))
                    }, opts._alsoResize_) {
                        var
                        optstest = "{'#gview_" + gID + " .ui-jqgrid-bdiv':true,'" + opts._alsoResize_ + "':true}";
                        opts.alsoResize = eval("(" + optstest + ")")
                    } else opts.alsoResize = $(".ui-jqgrid-bdiv", "#gview_" + gID);
                    delete
                    opts._alsoResize_, $("#gbox_" + gID).resizable(opts)
                }
            })
        }
    })
});
! function (a) {
    "use strict";
    "function" == typeof
    define && define.amd ? define(["jquery"], a) : a(jQuery)
}(function (a) {
    "use strict";
    var
    b, c = a();
    a.fn.html5sortable = function (d) {
        var
        e = String(d);
        return d = a.extend({
            connectWith: !1
        }, d), this.each(function () {
            var
            f;
            if (/^enable|disable|destroy$/.test(e)) return f = a(this).children(a(this).data("items")).attr("draggable", "enable" === e), void("destroy" === e && f.add(this).removeData("connectWith items").off("dragstart.h5s dragend.h5s selectstart.h5s dragover.h5s dragenter.h5s drop.h5s"));
            var
            g, h;
            f = a(this).children(d.items);
            var
            i = a("<" + (/^ul|ol$/i.test(this.tagName) ? "li" : /^tbody$/i.test(this.tagName) ? "tr" : "div") + ' class="sortable-placeholder ' + d.placeholderClass + '">').html("&nbsp;");
            f.find(d.handle).mousedown(function () {
                g = !0
            }).mouseup(function () {
                g = !1
            }), a(this).data("items", d.items), c = c.add(i), d.connectWith && a(d.connectWith).add(this).data("connectWith", d.connectWith), f.attr("draggable", "true").on("dragstart.h5s", function (c) {
                if (d.handle && !g) return !1;
                g = !1;
                var
                e = c.originalEvent.dataTransfer;
                e.effectAllowed = "move", e.setData("Text", "dummy"), h = (b = a(this)).addClass("sortable-dragging").index()
            }).on("dragend.h5s", function () {
                b && (b.removeClass("sortable-dragging").show(), c.detach(), h !== b.index() && b.parent().trigger("sortupdate", {
                    item: b,
                    startindex: h,
                    endindex: b.index()
                }), b = null)
            }).not("a[href], img").on("selectstart.h5s", function () {
                return this.dragDrop && this.dragDrop(), !1
            }).end().add([this, i]).on("dragover.h5s dragenter.h5s drop.h5s", function (e) {
                return !f.is(b) && d.connectWith !== a(b).parent().data("connectWith") || ("drop" === e.type ? (e.stopPropagation(), c.filter(":visible").after(b), b.trigger("dragend.h5s"), !1) : (e.preventDefault(), e.originalEvent.dataTransfer.dropEffect = "move", f.is(this) ? (d.forcePlaceholderSize && i.height(b.outerHeight()), b.hide(), a(this)[i.index() < a(this).index() ? "after" : "before"](i), c.not(i).detach()) : c.is(this) || a(this).children(d.items).length || (c.detach(), a(this).append(i)), !1))
            })
        })
    }
});
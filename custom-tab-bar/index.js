const normalizeRoute = (route = '') => route.replace(/^\//, '').split('?')[0]

Component({
  data: {
    selected: 0,
    color: "#999999",
    selectedColor: "#0071e3",
    list: [{
      pagePath: "pages/index/index",
      text: "首页",
      iconPath: "/static/tabbar/home.png",
      selectedIconPath: "/static/tabbar/home-active.png"
    }, {
      pagePath: "pages/community/index",
      text: "社区",
      iconPath: "/static/tabbar/community.png",
      selectedIconPath: "/static/tabbar/community-active.png"
    }, {
      pagePath: "pages/shop/index",
      text: "商城",
      iconPath: "/static/tabbar/shop.png",
      selectedIconPath: "/static/tabbar/shop-active.png"
    }, {
      pagePath: "pages/user/index",
      text: "我的",
      iconPath: "/static/tabbar/user.png",
      selectedIconPath: "/static/tabbar/user-active.png"
    }]
  },

  lifetimes: {
    attached() {
      this.registerGlobalRef()
      this.updateSelected()
    },
    detached() {
      this.unbindRouteListener()
    }
  },

  pageLifetimes: {
    show() {
      this.updateSelected()
    }
  },

  methods: {
    registerGlobalRef() {
      const app = getApp()
      if (app) {
        app.globalData = app.globalData || {}
        app.globalData.__customTabBar__ = this
      }
      this.bindRouteListener()
    },

    bindRouteListener() {
      if (this.__routeListenerBound || typeof wx === 'undefined' || typeof wx.onAppRoute !== 'function') return

      this.__routeListener = (routeInfo = {}) => {
        const path = routeInfo.path || routeInfo.route
        if (!path) return
        this.scheduleRouteUpdate(path)
      }

      wx.onAppRoute(this.__routeListener)
      this.__routeListenerBound = true
    },

    unbindRouteListener() {
      if (this.__routeListener && typeof wx !== 'undefined' && typeof wx.offAppRoute === 'function') {
        wx.offAppRoute(this.__routeListener)
      }
      this.__routeListener = null
      this.__routeListenerBound = false
      if (this.__routeTimer) {
        clearTimeout(this.__routeTimer)
        this.__routeTimer = null
      }
    },

    scheduleRouteUpdate(route) {
      if (this.__routeTimer) {
        clearTimeout(this.__routeTimer)
      }
      this.__routeTimer = setTimeout(() => {
        this.updateSelectedByRoute(route)
        this.__routeTimer = null
      }, 40)
    },

    updateSelected() {
      const pages = getCurrentPages()
      if (!pages || !pages.length) return

      const currentPage = pages[pages.length - 1]
      const route = currentPage?.route || currentPage?.__route__
      this.updateSelectedByRoute(route)
    },

    updateSelectedByRoute(route = '') {
      const normalizedRoute = normalizeRoute(route)
      if (!normalizedRoute) return

      const targetIndex = this.data.list.findIndex(item => {
        return normalizeRoute(item.pagePath) === normalizedRoute
      })

      if (targetIndex !== -1 && targetIndex !== this.data.selected) {
        this.setData({ selected: targetIndex })
      }

      if (targetIndex !== -1) {
        this.__currentRoute = normalizedRoute
      }
    },

    switchTab(e) {
      const data = e.currentTarget.dataset
      const index = data.index
      const targetRoute = normalizeRoute(data.path || '')
      const url = '/' + targetRoute

      this.setData({ selected: index })
      this.__currentRoute = targetRoute
      wx.switchTab({ url })
    }
  }
})

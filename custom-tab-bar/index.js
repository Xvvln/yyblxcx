const normalizeRoute = (route = '') => route.replace(/^\//, '').split('?')[0]

const normalizeIndex = (value) => {
  if (value === '' || value === null || value === undefined) return null
  const num = Number(value)
  return Number.isNaN(num) ? null : num
}

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
    created() {
      this.__selectedIndex = this.data.selected || 0
      this.__currentRoute = null
      this.__prevRoute = null
      this.__ignoreRouteInfo = null
      this.__pendingRoute = null
    },
    attached() {
      this.registerGlobalRef()
      this.syncSelectedWithCurrentRoute()
      this.bindRouteListener()
    },
    detached() {
      this.unbindRouteListener()
    }
  },

  methods: {
    shouldIgnoreRoute(route = '') {
      const info = this.__ignoreRouteInfo
      if (!info || info.route !== route) return false
      if (Date.now() > info.until) {
        this.__ignoreRouteInfo = null
        return false
      }
      return true
    },

    setIgnoreRoute(route) {
      if (!route) {
        this.__ignoreRouteInfo = null
        return
      }
      this.__ignoreRouteInfo = {
        route,
        until: Date.now() + 300 // 忽略上一页 300ms，避免迟到的回调拉扯滑块
      }
    },

    registerGlobalRef() {
      const app = getApp()
      if (app) {
        app.globalData = app.globalData || {}
        app.globalData.__customTabBar__ = this
      }
    },

    applySelected(index) {
      if (typeof index !== 'number' || index < 0 || index >= this.data.list.length) return
      if (this.__selectedIndex === index) return
      this.__selectedIndex = index
      this.setData({ selected: index })
    },

    syncSelectedWithCurrentRoute() {
      const pages = getCurrentPages()
      if (!pages || !pages.length) return

      const currentPage = pages[pages.length - 1]
      const route = currentPage?.route || currentPage?.__route__
      this.updateSelectedByRoute(route)
      this.__currentRoute = normalizeRoute(route || '')
      this.__prevRoute = null
      this.__pendingRoute = null
      this.__ignoreRouteInfo = null
    },

    bindRouteListener() {
      if (this.__routeListenerBound || typeof wx === 'undefined' || typeof wx.onAppRoute !== 'function') return

      this.__routeListener = (routeInfo = {}) => {
        const path = routeInfo.path || routeInfo.route
        if (!path) return
        this.handleRouteChange(path)
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
    },

    handleRouteChange(route) {
      const normalizedRoute = normalizeRoute(route)
      if (!normalizedRoute) return

      if (this.shouldIgnoreRoute(normalizedRoute)) {
        return
      }

      const targetIndex = this.findIndexByRoute(normalizedRoute)
      if (targetIndex === -1) return

      if (this.__pendingRoute) {
        if (normalizedRoute !== this.__pendingRoute) {
          // 等待指定页面出现，忽略其它路由回调
          return
        }

        this.__pendingRoute = null
        this.setIgnoreRoute(this.__prevRoute)
        this.__currentRoute = normalizedRoute
        this.__prevRoute = null
        this.applySelected(targetIndex)
        return
      }

      if (normalizedRoute === this.__currentRoute) {
        // 重复回调
        return
      }

      this.setIgnoreRoute(this.__currentRoute)
      this.__prevRoute = this.__currentRoute
      this.__currentRoute = normalizedRoute
      this.applySelected(targetIndex)
    },

    updateSelectedByRoute(route = '') {
      const normalizedRoute = normalizeRoute(route)
      if (!normalizedRoute) return
      const targetIndex = this.findIndexByRoute(normalizedRoute)
      if (targetIndex !== -1) {
        this.applySelected(targetIndex)
        this.__currentRoute = normalizedRoute
        this.__prevRoute = null
      }
    },

    findIndexByRoute(route) {
      return this.data.list.findIndex(item => normalizeRoute(item.pagePath) === route)
    },

    switchTab(e) {
      const data = e.currentTarget.dataset
      const index = normalizeIndex(data.index)
      if (index === null) return

      const path = data.path || ''
      const url = '/' + normalizeRoute(path)

      const normalizedRoute = normalizeRoute(path)
      this.__pendingRoute = normalizedRoute
      this.__prevRoute = this.__currentRoute
      this.__ignoreRouteInfo = null

      this.applySelected(index)
      wx.switchTab({ url })
    }
  }
})

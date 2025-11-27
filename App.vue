<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
			// 启动时检查登录状态
			const token = uni.getStorageSync('token')
			if (!token) {
				// 未登录，延迟跳转登录页（确保页面栈已初始化）
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/login/index'
					})
				}, 100)
			}
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	/*每个页面公共css */
	:root {
		// 主色
		--color-primary: #0071e3;
		--color-success: #34C759;
		--color-warning: #FF9500;
		--color-error: #FF3B30;
		
		// 背景
		--bg-page: #F5F5F7;
		--bg-card: #FFFFFF;
		
		// 文字
		--text-primary: #1D1D1F;
		--text-secondary: #86868B;
		--text-placeholder: #C7C7CC;
		
		// 边框
		--border-color: #E5E5E5;
        
        // 圆角
        --border-radius-small: 8px;
        --border-radius-medium: 12px;
        --border-radius-large: 16px;
	}

    page {
        background-color: var(--bg-page);
        color: var(--text-primary);
        font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif;
    }

    /* 图标占位符 */
    .icon-placeholder {
        background-color: #E5E5E5;
        border-radius: 8rpx;
        display: inline-block;
    }

    /* 图片占位符 */
    .image-placeholder {
        background-color: #F5F5F7;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--text-secondary);
        font-size: 24rpx;
    }
</style>

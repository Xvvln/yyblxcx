<template>
  <view class="page">
    <!-- 导航栏 -->
    <view class="nav-bar">
      <view class="back-btn" @click="goBack">
        <wd-icon name="arrow-left" size="20px" color="#1D1D1F"></wd-icon>
      </view>
      <text class="nav-title">购物车</text>
      <view class="edit-btn" @click="toggleEdit">
        <text>{{ isEdit ? '完成' : '编辑' }}</text>
      </view>
    </view>
    
    <!-- 购物车列表 -->
    <scroll-view scroll-y class="cart-scroll" v-if="cartList.length > 0">
      <view class="cart-item" v-for="item in cartList" :key="item.id">
        <view class="checkbox" :class="{ checked: item.is_selected }" @click="toggleItem(item)">
          <wd-icon v-if="item.is_selected" name="check" size="14px" color="#FFFFFF"></wd-icon>
        </view>
        
        <view class="product-image">
          <image v-if="item.product?.image" :src="item.product.image" mode="aspectFill" />
          <text v-else class="placeholder">图</text>
        </view>
        
        <view class="product-info">
          <text class="name">{{ item.product?.name }}</text>
          <view class="bottom-row">
            <text class="price">¥{{ item.product?.price }}</text>
            <view class="quantity-control">
              <view class="qty-btn" @click="changeQuantity(item, -1)">
                <wd-icon name="decrease" size="16px" color="#86868B"></wd-icon>
              </view>
              <text class="qty-num">{{ item.quantity }}</text>
              <view class="qty-btn" @click="changeQuantity(item, 1)">
                <wd-icon name="add" size="16px" color="#1D1D1F"></wd-icon>
              </view>
            </view>
          </view>
        </view>
        
        <view class="delete-btn" v-if="isEdit" @click="deleteItem(item.id)">
          <wd-icon name="delete" size="20px" color="#FF3B30"></wd-icon>
        </view>
      </view>
    </scroll-view>
    
    <!-- 空购物车 -->
    <view class="empty" v-else>
      <text class="empty-icon">🛒</text>
      <text class="empty-text">购物车是空的</text>
      <button class="shop-btn" @click="goShop">去逛逛</button>
    </view>
    
    <!-- 底部结算栏 -->
    <view class="footer" v-if="cartList.length > 0">
      <view class="select-all" @click="toggleAll">
        <view class="checkbox" :class="{ checked: allSelected }">
          <wd-icon v-if="allSelected" name="check" size="14px" color="#FFFFFF"></wd-icon>
        </view>
        <text>全选</text>
      </view>
      
      <view class="total-area">
        <text class="total-label">合计:</text>
        <text class="total-price">¥{{ totalPrice }}</text>
      </view>
      
      <button 
        class="checkout-btn" 
        :disabled="selectedCount === 0"
        @click="checkout"
      >
        结算({{ selectedCount }})
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getCartList, updateCartItem, deleteCartItem } from '@/api/shop'

interface CartItem {
  id: number
  product_id: number
  quantity: number
  is_selected: number
  product?: {
    name: string
    image?: string
    price: number
    original_price?: number
    stock: number
    is_on_sale?: number
  }
  subtotal?: number
  is_valid?: boolean
}

const cartList = ref<CartItem[]>([])
const isEdit = ref(false)
const loading = ref(false)

const allSelected = computed(() => {
  return cartList.value.length > 0 && cartList.value.every(item => item.is_selected)
})

const selectedCount = computed(() => {
  return cartList.value.filter(item => item.is_selected).length
})

const totalPrice = computed(() => {
  return cartList.value
    .filter(item => item.is_selected)
    .reduce((sum, item) => sum + (item.product?.price || 0) * item.quantity, 0)
    .toFixed(2)
})

// 获取购物车列表
async function fetchCartList() {
  loading.value = true
  try {
    const res = await getCartList()
    if (res.code === 200) {
      cartList.value = res.data?.list || []
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 切换编辑模式
function toggleEdit() {
  isEdit.value = !isEdit.value
}

// 切换单个商品选中
async function toggleItem(item: CartItem) {
  try {
    const newSelected = item.is_selected ? 0 : 1
    await updateCartItem(item.id, { is_selected: newSelected })
    item.is_selected = newSelected
  } catch (e) {
    console.error(e)
  }
}

// 全选/取消全选
async function toggleAll() {
  const newSelected = allSelected.value ? 0 : 1
  try {
    await Promise.all(
      cartList.value.map(item => updateCartItem(item.id, { is_selected: newSelected }))
    )
    cartList.value.forEach(item => item.is_selected = newSelected)
  } catch (e) {
    console.error(e)
  }
}

// 修改数量
async function changeQuantity(item: CartItem, delta: number) {
  const newQty = item.quantity + delta
  if (newQty < 1) {
    // 删除
    uni.showModal({
      title: '提示',
      content: '确定删除该商品吗？',
      success: async (res) => {
        if (res.confirm) {
          await deleteItem(item.id)
        }
      }
    })
    return
  }
  
  if (item.product && newQty > (item.product.stock || 999)) {
    uni.showToast({ title: '库存不足', icon: 'none' })
    return
  }
  
  try {
    await updateCartItem(item.id, { quantity: newQty })
    item.quantity = newQty
  } catch (e: any) {
    uni.showToast({ title: e.message || '修改失败', icon: 'none' })
  }
}

// 删除商品
async function deleteItem(id: number) {
  try {
    await deleteCartItem(id)
    cartList.value = cartList.value.filter(item => item.id !== id)
    uni.showToast({ title: '已删除', icon: 'success' })
  } catch (e: any) {
    uni.showToast({ title: e.message || '删除失败', icon: 'none' })
  }
}

// 结算
function checkout() {
  if (selectedCount.value === 0) {
    uni.showToast({ title: '请选择商品', icon: 'none' })
    return
  }
  
  // 传递选中的商品ID
  const selectedIds = cartList.value
    .filter(item => item.is_selected)
    .map(item => item.id)
    .join(',')
  
  uni.navigateTo({ url: `/pages/order/confirm?cart_ids=${selectedIds}` })
}

function goBack() {
  uni.navigateBack()
}

function goShop() {
  uni.switchTab({ url: '/pages/shop/index' })
}

onShow(() => {
  fetchCartList()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding-bottom: 80px;
}

.nav-bar {
  height: 44px;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  padding-top: var(--status-bar-height);
  box-sizing: content-box;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .back-btn {
    padding: 8px;
  }
  
  .nav-title {
    font-size: 17px;
    font-weight: 600;
    color: #1D1D1F;
  }
  
  .edit-btn {
    padding: 8px;
    font-size: 14px;
    color: #0071e3;
  }
}

.cart-scroll {
  padding: 16px;
}

.cart-item {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  
  .checkbox {
    width: 22px;
    height: 22px;
    border: 2px solid #E5E5EA;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
    flex-shrink: 0;
    
    &.checked {
      background: #0071e3;
      border-color: #0071e3;
    }
  }
  
  .product-image {
    width: 80px;
    height: 80px;
    background: #F5F5F7;
    border-radius: 12px;
    margin-right: 12px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    
    image {
      width: 100%;
      height: 100%;
    }
    
    .placeholder {
      color: #C7C7CC;
      font-size: 12px;
    }
  }
  
  .product-info {
    flex: 1;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    
    .name {
      font-size: 14px;
      color: #1D1D1F;
      font-weight: 500;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
    }
    
    .spec {
      font-size: 12px;
      color: #86868B;
    }
    
    .bottom-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .price {
        font-size: 16px;
        font-weight: 700;
        color: #FF3B30;
      }
      
      .quantity-control {
        display: flex;
        align-items: center;
        gap: 12px;
        
        .qty-btn {
          width: 28px;
          height: 28px;
          background: #F5F5F7;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .qty-num {
          font-size: 15px;
          font-weight: 600;
          color: #1D1D1F;
          min-width: 24px;
          text-align: center;
        }
      }
    }
  }
  
  .delete-btn {
    padding: 8px;
    margin-left: 8px;
  }
}

.empty {
  padding: 100px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
  }
  
  .empty-text {
    font-size: 15px;
    color: #86868B;
    margin-bottom: 24px;
  }
  
  .shop-btn {
    width: 120px;
    height: 40px;
    background: #0071e3;
    border-radius: 20px;
    border: none;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 500;
    
    &::after {
      border: none;
    }
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  padding: 0 16px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  
  .select-all {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #1D1D1F;
    
    .checkbox {
      width: 20px;
      height: 20px;
      border: 2px solid #E5E5EA;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.checked {
        background: #0071e3;
        border-color: #0071e3;
      }
    }
  }
  
  .total-area {
    flex: 1;
    text-align: right;
    margin-right: 16px;
    
    .total-label {
      font-size: 14px;
      color: #1D1D1F;
    }
    
    .total-price {
      font-size: 20px;
      font-weight: 700;
      color: #FF3B30;
      margin-left: 4px;
    }
  }
  
  .checkout-btn {
    width: 100px;
    height: 40px;
    background: #0071e3;
    border-radius: 20px;
    border: none;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 600;
    
    &::after {
      border: none;
    }
    
    &[disabled] {
      background: #E5E5EA;
      color: #86868B;
    }
  }
}
</style>

<template>
  <view class="page">
    <view class="article" v-if="article">
      <text class="title">{{ article.title }}</text>
      <view class="meta">
        <text class="author">{{ article.author }}</text>
        <text class="date">{{ article.date }}</text>
        <text class="views">{{ article.views }}阅读</text>
      </view>
      <view class="content">
        <text>{{ article.content }}</text>
      </view>
      <view class="tags" v-if="article.tags?.length">
        <text class="tag" v-for="tag in article.tags" :key="tag"># {{ tag }}</text>
      </view>
    </view>
    
    <!-- 相关推荐 -->
    <view class="recommend-section" v-if="relatedArticles.length">
      <text class="section-title">相关推荐</text>
      <view class="article-item" v-for="item in relatedArticles" :key="item.id" @click="viewArticle(item.id)">
        <text class="item-title">{{ item.title }}</text>
        <text class="item-views">{{ item.views }}阅读</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

interface Article {
  id: number
  title: string
  author: string
  date: string
  views: number
  content: string
  tags?: string[]
}

const articleId = ref(0)
const article = ref<Article | null>(null)
const relatedArticles = ref<any[]>([])

// 模拟文章数据
const articlesData: Record<number, Article> = {
  1: {
    id: 1,
    title: '如何科学减脂不反弹？',
    author: '王医生',
    date: '2025-11-20',
    views: 2300,
    content: `很多人在减脂过程中都会遇到反弹的问题，这往往是因为减脂方法不科学导致的。今天我们就来聊聊如何科学减脂，避免反弹。

1. 制定合理的热量缺口
每天的热量缺口控制在300-500大卡比较合适，过大的热量缺口会导致身体进入"节能模式"，反而不利于减脂。

2. 保证蛋白质摄入
减脂期间每公斤体重摄入1.6-2.2克蛋白质，可以帮助保持肌肉量，提高基础代谢。

3. 规律运动
建议每周进行3-5次运动，包括有氧和力量训练。力量训练可以增加肌肉量，提高基础代谢。

4. 保证充足睡眠
睡眠不足会影响瘦素分泌，导致食欲增加。建议每天保证7-8小时睡眠。

5. 控制减脂速度
每周减重0.5-1公斤是比较健康的速度，过快的减重速度容易导致反弹。

6. 建立长期的饮食习惯
减脂成功后不要立即恢复高热量饮食，要逐步增加热量摄入，让身体有一个适应过程。`,
    tags: ['减脂', '健康饮食', '科学运动']
  },
  2: {
    id: 2,
    title: '春季流感预防指南',
    author: '李医生',
    date: '2025-11-18',
    views: 1500,
    content: `春季是流感高发季节，做好预防工作非常重要。以下是一些实用的预防措施：

1. 接种流感疫苗
这是预防流感最有效的方法，建议每年秋季接种。

2. 勤洗手
使用肥皂和流动水洗手至少20秒，特别是在触摸公共物品后。

3. 保持室内通风
每天开窗通风2-3次，每次20-30分钟。

4. 避免接触患者
尽量避免与流感患者密切接触，如需接触应佩戴口罩。

5. 增强免疫力
- 保证充足睡眠
- 均衡饮食，多吃蔬果
- 适量运动
- 保持良好心态

6. 注意个人卫生
- 不要用手触摸眼、鼻、口
- 咳嗽或打喷嚏时用纸巾遮挡
- 使用过的纸巾及时丢弃

7. 出现症状及时就医
如果出现发热、咳嗽、头痛等症状，应及时就医，不要自行服药。`,
    tags: ['流感', '预防', '春季健康']
  }
}

onLoad((options) => {
  articleId.value = Number(options?.id || 0)
  loadArticle()
})

function loadArticle() {
  // 获取文章详情
  article.value = articlesData[articleId.value] || {
    id: articleId.value,
    title: '文章详情',
    author: '未知作者',
    date: '2025-11-20',
    views: 0,
    content: '文章内容加载中...'
  }
  
  // 加载相关推荐
  relatedArticles.value = Object.values(articlesData)
    .filter(a => a.id !== articleId.value)
    .slice(0, 3)
}

function viewArticle(id: number) {
  uni.redirectTo({ url: `/pages/doctor/article?id=${id}` })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-bottom: 40px;
}

.article {
  background: #FFFFFF;
  padding: 20px;
  margin-bottom: 12px;
  
  .title {
    font-size: 22px;
    font-weight: 700;
    color: #1D1D1F;
    line-height: 1.4;
    display: block;
    margin-bottom: 16px;
  }
  
  .meta {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #F5F5F7;
    
    text {
      font-size: 13px;
      color: #86868B;
    }
  }
  
  .content {
    text {
      font-size: 16px;
      color: #1D1D1F;
      line-height: 1.8;
      white-space: pre-wrap;
    }
  }
  
  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid #F5F5F7;
    
    .tag {
      background: #E8F4FD;
      color: #0071e3;
      font-size: 12px;
      padding: 6px 12px;
      border-radius: 16px;
    }
  }
}

.recommend-section {
  background: #FFFFFF;
  padding: 20px;
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 16px;
    display: block;
  }
  
  .article-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid #F5F5F7;
    
    &:last-child {
      border-bottom: none;
    }
    
    .item-title {
      font-size: 14px;
      color: #1D1D1F;
      flex: 1;
      margin-right: 12px;
    }
    
    .item-views {
      font-size: 12px;
      color: #86868B;
    }
  }
}
</style>













/**
 * Mock Data Definitions
 */

export const MOCK_DATA: Record<string, any> = {
  // 用户信息
  '/user/profile': {
    code: 200,
    message: 'success',
    data: {
      id: 'u_123456',
      nickname: '健康达人',
      avatar: '',
      phone: '13800138000',
      gender: 1,
      age: 25,
      height: 175,
      weight: 65,
      sport_coins: 1280,
      food_coins: 350,
      vip_level: 1,
      vip_expire_time: '2025-12-31'
    }
  },

  // 首页数据
  '/home/dashboard': {
    code: 200,
    message: 'success',
    data: {
      daily_tasks: [
        { id: 1, title: '完成一次健康筛查', status: 0, reward: 50 },
        { id: 2, title: '记录今日饮食', status: 1, reward: 20 }
      ],
      health_score: 85,
      calories_burned: 350,
      steps: 5600
    }
  },

  // 社区动态
  '/community/posts': {
    code: 200,
    message: 'success',
    data: {
      list: [
        {
          id: 'p_1',
          user: { nickname: 'RunningMan', avatar: '' },
          content: '今天跑了5公里，感觉很棒！#跑步 #健康',
          images: [],
          likes: 120,
          comments: 15,
          create_time: '2小时前'
        },
        {
          id: 'p_2',
          user: { nickname: 'HealthyFood', avatar: '' },
          content: '分享今日的减脂午餐，鸡胸肉沙拉。',
          images: [],
          likes: 85,
          comments: 8,
          create_time: '4小时前'
        }
      ]
    }
  },

  // 健康筛查记录
  '/health/records': {
    code: 200,
    message: 'success',
    data: {
      list: [
        { id: 123, date: '2025-11-27', risk_level: 'low' },
        { id: 101, date: '2025-11-20', risk_level: 'medium' }
      ]
    }
  },

  // 筛查报告详情 (Mock ID 123)
  '/health/report/123': {
    code: 200,
    message: 'success',
    data: {
      id: 123,
      date: '2025-11-27',
      risk_level: 'low',
      score: 92,
      suggestion: '您的营养状况良好。根据GLIM标准评估，您当前没有明显的营养不良风险。建议继续保持均衡饮食，适量增加优质蛋白摄入。',
      diet_plan: '建议每日摄入蛋白质 60-70g，多吃深色蔬菜和全谷物。',
      exercise_plan: '建议每周进行 150 分钟中等强度有氧运动，如快走、游泳。'
    }
  },

  // 筛查提交响应
  '/health/screening': {
    code: 200,
    message: 'success',
    data: {
        id: 123
    }
  }
}

'use client'

import { Card, Form, Input, Button, Typography, Divider } from 'antd'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

const { Title, Text } = Typography

export default function SignIn() {
  const router = useRouter()

  const handleSubmit = (values: { email: string; password: string }) => {
    // Here you would typically handle authentication
    console.log('Form submitted:', values)
    // For now, just redirect to dashboard
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <Title level={2}>PEA Protein Analysis</Title>
          <Title level={3}>Sign in to your account</Title>
          <Text type="secondary">
            Use admin@admin.com / admin to sign in
          </Text>
        </div>

        <Form
          name="signin"
          layout="vertical"
          onFinish={handleSubmit}
          requiredMark="optional"
        >
          <Form.Item
            label="Email address"
            name="email"
            rules={[
              { required: true, message: 'Please input your email!' },
              { type: 'email', message: 'Please enter a valid email!' },
            ]}
          >
            <Input size="large" />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password size="large" />
          </Form.Item>

          <div className="text-right mb-4">
            <Link
              href="/forgot-password"
              className="text-blue-600 hover:text-blue-500"
            >
              Forgot your password?
            </Link>
          </div>

          <Form.Item>
            <Button type="primary" htmlType="submit" size="large" block>
              Sign in
            </Button>
          </Form.Item>

          <Divider>or</Divider>

          <div className="text-center">
            <Text>Don't have an account? </Text>
            <Link href="/signup" className="text-blue-600 hover:text-blue-500">
              Sign up
            </Link>
          </div>
        </Form>
      </Card>
    </div>
  )
} 
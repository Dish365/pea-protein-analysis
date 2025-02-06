"use client";

import React from "react";
import { Form, Input, Button, Card, message } from "antd";
import { MailOutlined } from "@ant-design/icons";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

export default function ForgotPasswordPage() {
  const { resetPassword } = useAuth();
  const [loading, setLoading] = React.useState(false);
  const [sent, setSent] = React.useState(false);

  const onFinish = async (values: { email: string }) => {
    try {
      setLoading(true);
      await resetPassword(values.email);
      setSent(true);
      message.success("Password reset instructions sent to your email");
    } catch (error: any) {
      message.error(error.message || "Failed to send reset instructions");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="max-w-md w-full">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold">Reset Password</h2>
          <p className="mt-2 text-gray-600">
            Enter your email to receive reset instructions
          </p>
        </div>

        {!sent ? (
          <Form
            name="forgot-password"
            onFinish={onFinish}
            layout="vertical"
            requiredMark={false}
          >
            <Form.Item
              name="email"
              rules={[
                { required: true, message: "Please input your email" },
                { type: "email", message: "Please enter a valid email" },
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="Email"
                size="large"
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                block
                loading={loading}
              >
                Send Reset Instructions
              </Button>
            </Form.Item>
          </Form>
        ) : (
          <div className="text-center">
            <p className="text-green-600 mb-4">
              Check your email for password reset instructions
            </p>
            <Button type="link" onClick={() => setSent(false)}>
              Try another email
            </Button>
          </div>
        )}

        <div className="text-center mt-4">
          <Link
            href="/signin"
            className="text-blue-600 hover:text-blue-800"
          >
            Back to Sign In
          </Link>
        </div>
      </Card>
    </div>
  );
} 
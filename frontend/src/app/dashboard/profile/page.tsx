"use client";

import React, { useState } from "react";
import { Card, Tabs, Form, Input, Button, message, Avatar } from "antd";
import { UserOutlined, LockOutlined, MailOutlined } from "@ant-design/icons";
import { useUser } from "@/hooks/useUser";

const { TabPane } = Tabs;

export default function ProfilePage() {
  const [loading, setLoading] = useState(false);
  const { user, updateUser } = useUser();
  const [form] = Form.useForm();

  const handleUpdateProfile = async (values: any) => {
    try {
      setLoading(true);
      await updateUser(values);
      message.success("Profile updated successfully");
    } catch (error: any) {
      message.error(error.message || "Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Profile Settings</h1>
      
      <Card>
        <Tabs defaultActiveKey="profile">
          <TabPane tab="Profile Information" key="profile">
            <div className="flex flex-col items-center mb-6">
              <Avatar size={100} icon={<UserOutlined />} />
              <h2 className="mt-4 text-lg font-medium">{user?.name}</h2>
              <p className="text-gray-500">{user?.role}</p>
            </div>

            <Form
              form={form}
              layout="vertical"
              onFinish={handleUpdateProfile}
              initialValues={user}
            >
              <Form.Item
                label="Full Name"
                name="name"
                rules={[{ required: true }]}
              >
                <Input prefix={<UserOutlined />} />
              </Form.Item>

              <Form.Item
                label="Email"
                name="email"
                rules={[
                  { required: true },
                  { type: "email", message: "Please enter a valid email" },
                ]}
              >
                <Input prefix={<MailOutlined />} />
              </Form.Item>

              <Form.Item label="Organization" name="organization">
                <Input />
              </Form.Item>

              <Form.Item label="Job Title" name="jobTitle">
                <Input />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  block
                >
                  Update Profile
                </Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane tab="Security" key="security">
            <Form layout="vertical" onFinish={handleUpdateProfile}>
              <Form.Item
                label="Current Password"
                name="currentPassword"
                rules={[{ required: true }]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item
                label="New Password"
                name="newPassword"
                rules={[{ required: true, min: 8 }]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item
                label="Confirm Password"
                name="confirmPassword"
                dependencies={["newPassword"]}
                rules={[
                  { required: true },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue("newPassword") === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject("Passwords do not match");
                    },
                  }),
                ]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  block
                >
                  Update Password
                </Button>
              </Form.Item>
            </Form>
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
} 
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { api, MinerDetail as MinerDetailType, HashboardInfo } from '../api/client';
import './MinerDetail.css';

const MinerDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [miner, setMiner] = useState<MinerDetailType | null>(null);
  const [loading, setLoading] = useState(true);

  const loadMinerDetail = useCallback(async () => {
    if (!id) return;
    try {
      const data = await api.getMinerDetail(parseInt(id));
      setMiner(data);
      setLoading(false);
    } catch (error) {
      console.error('加载矿机详情失败:', error);
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (id) {
      loadMinerDetail();
      const interval = setInterval(loadMinerDetail, 30000);
      return () => clearInterval(interval);
    }
  }, [id, loadMinerDetail]);

  const formatHashrate = (th: number | null): string => {
    if (!th) return '0 TH/s';
    return `${th.toFixed(2)} TH/s`;
  };

  const formatUptime = (seconds: number | null): string => {
    if (!seconds) return '0秒';
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (days > 0) return `${days}天 ${hours}小时 ${mins}分钟`;
    if (hours > 0) return `${hours}小时 ${mins}分钟`;
    return `${mins}分钟`;
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
  };

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  if (!miner) {
    return <div className="error">矿机不存在</div>;
  }

  const status = miner.latest_status;

  // 准备图表数据
  const chartData = miner.history.map((point) => ({
    time: new Date(point.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    temp_chip: point.temp_chip || 0,
    temp_pcb: point.temp_pcb || 0,
    hashrate: point.hashrate || 0,
    power: point.power_consumption || 0,
  }));

  return (
    <div className="miner-detail">
      <div className="detail-header">
        <button className="back-btn" onClick={() => navigate('/')}>
          ← 返回
        </button>
        <div>
          <h2>{miner.hostname || miner.ip_address}</h2>
          <p className="miner-info">{miner.model || '未知型号'} | {miner.ip_address}</p>
        </div>
      </div>

      {status && (
        <>
          <div className="status-grid">
            <div className="status-card">
              <h3>温度信息</h3>
              <div className="status-content">
                <div className="status-item">
                  <span className="label">芯片温度:</span>
                  <span className="value">{status.temp_chip || '--'}°C</span>
                </div>
                <div className="status-item">
                  <span className="label">PCB温度:</span>
                  <span className="value">{status.temp_pcb || '--'}°C</span>
                </div>
                <div className="status-item">
                  <span className="label">最高温度:</span>
                  <span className="value">{status.temp_max || '--'}°C</span>
                </div>
              </div>
            </div>

            <div className="status-card">
              <h3>算力信息</h3>
              <div className="status-content">
                <div className="status-item">
                  <span className="label">5秒算力:</span>
                  <span className="value">{formatHashrate(status.hashrate_5s)}</span>
                </div>
                <div className="status-item">
                  <span className="label">平均算力:</span>
                  <span className="value">{formatHashrate(status.hashrate_avg)}</span>
                </div>
                <div className="status-item">
                  <span className="label">总算力:</span>
                  <span className="value">{formatHashrate(status.hashrate)}</span>
                </div>
              </div>
            </div>

            <div className="status-card">
              <h3>功耗与湿度</h3>
              <div className="status-content">
                <div className="status-item">
                  <span className="label">功耗:</span>
                  <span className="value">{status.power_consumption?.toFixed(0) || '--'} W</span>
                </div>
                <div className="status-item">
                  <span className="label">湿度:</span>
                  <span className="value">{status.humidity || '--'}%</span>
                </div>
              </div>
            </div>

            <div className="status-card">
              <h3>风扇转速</h3>
              <div className="status-content">
                {[status.fan_speed_1, status.fan_speed_2, status.fan_speed_3, status.fan_speed_4]
                  .filter((speed) => speed !== null)
                  .map((speed, index) => (
                    <div key={index} className="status-item">
                      <span className="label">风扇 {index + 1}:</span>
                      <span className="value">{speed} RPM</span>
                    </div>
                  ))}
              </div>
            </div>

            <div className="status-card">
              <h3>矿池信息</h3>
              <div className="status-content">
                <div className="status-item">
                  <span className="label">矿池URL:</span>
                  <span className="value">{status.pool_url || '--'}</span>
                </div>
                <div className="status-item">
                  <span className="label">用户名:</span>
                  <span className="value">{status.pool_user || '--'}</span>
                </div>
                <div className="status-item">
                  <span className="label">连接状态:</span>
                  <span className={`value ${status.pool_status === 'Alive' ? 'online' : 'offline'}`}>
                    {status.pool_status || '未知'}
                  </span>
                </div>
              </div>
            </div>

            <div className="status-card">
              <h3>运行信息</h3>
              <div className="status-content">
                <div className="status-item">
                  <span className="label">运行时间:</span>
                  <span className="value">{formatUptime(status.uptime)}</span>
                </div>
                <div className="status-item">
                  <span className="label">网络状态:</span>
                  <span className={`value ${status.network_status === 'online' ? 'online' : 'offline'}`}>
                    {status.network_status || '未知'}
                  </span>
                </div>
                <div className="status-item">
                  <span className="label">最后更新:</span>
                  <span className="value">{formatDate(status.timestamp)}</span>
                </div>
              </div>
            </div>
          </div>

          {status.hasboard_info && status.hasboard_info.length > 0 && (
            <div className="hashboard-section">
              <h3>算力板信息</h3>
              <div className="hashboard-grid">
                {status.hasboard_info.map((board: HashboardInfo, index: number) => (
                  <div key={index} className="hashboard-card">
                    <h4>算力板 {board.id}</h4>
                    <div className="hashboard-info">
                      <div className="info-item">
                        <span>状态:</span>
                        <span className={board.status === 'Alive' ? 'online' : 'offline'}>
                          {board.status}
                        </span>
                      </div>
                      <div className="info-item">
                        <span>温度:</span>
                        <span>{board.temperature}°C</span>
                      </div>
                      <div className="info-item">
                        <span>芯片温度:</span>
                        <span>{board.chip_temp}°C</span>
                      </div>
                      <div className="info-item">
                        <span>PCB温度:</span>
                        <span>{board.pcb_temp}°C</span>
                      </div>
                      <div className="info-item">
                        <span>算力:</span>
                        <span>{board.hashrate}</span>
                      </div>
                      <div className="info-item">
                        <span>风扇转速:</span>
                        <span>{board.fan_speed} RPM</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {chartData.length > 0 && (
            <div className="chart-section">
              <h3>历史趋势</h3>
              <div className="charts">
                <div className="chart-card">
                  <h4>温度趋势</h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="temp_chip" stroke="#8884d8" name="芯片温度" />
                      <Line type="monotone" dataKey="temp_pcb" stroke="#82ca9d" name="PCB温度" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="chart-card">
                  <h4>算力趋势</h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="hashrate" stroke="#ffc658" name="算力 (TH/s)" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="chart-card">
                  <h4>功耗趋势</h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="power" stroke="#ff7300" name="功耗 (W)" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {miner.logs && miner.logs.length > 0 && (
        <div className="logs-section">
          <h3>运行日志</h3>
          <div className="logs-container">
            {miner.logs.map((log) => (
              <div key={log.id} className={`log-entry ${log.log_level.toLowerCase()}`}>
                <div className="log-header">
                  <span className="log-time">{formatDate(log.timestamp)}</span>
                  <span className={`log-level ${log.log_level.toLowerCase()}`}>
                    {log.log_level}
                  </span>
                </div>
                <div className="log-message">{log.message}</div>
                {log.source && <div className="log-source">来源: {log.source}</div>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MinerDetail;

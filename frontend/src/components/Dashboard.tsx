import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, Miner, Stats } from '../api/client';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const [miners, setMiners] = useState<Miner[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [discovering, setDiscovering] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000); // 每30秒刷新
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [minersData, statsData] = await Promise.all([
        api.getMiners(),
        api.getStats(),
      ]);
      setMiners(minersData);
      setStats(statsData);
      setLoading(false);
    } catch (error) {
      console.error('加载数据失败:', error);
      setLoading(false);
    }
  };

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      await api.discoverMiners();
      await loadData();
    } catch (error) {
      console.error('发现矿机失败:', error);
    } finally {
      setDiscovering(false);
    }
  };

  const formatHashrate = (th: number | null): string => {
    if (!th) return '0 TH/s';
    return `${th.toFixed(2)} TH/s`;
  };

  const formatUptime = (seconds: number | null): string => {
    if (!seconds) return '0秒';
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (days > 0) return `${days}天 ${hours}小时`;
    if (hours > 0) return `${hours}小时 ${mins}分钟`;
    return `${mins}分钟`;
  };

  const getStatusColor = (isOnline: boolean): string => {
    return isOnline ? '#10b981' : '#ef4444';
  };

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="stats-cards">
          <div className="stat-card">
            <div className="stat-label">总矿机数</div>
            <div className="stat-value">{stats?.total_miners || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">在线</div>
            <div className="stat-value online">{stats?.online_miners || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">离线</div>
            <div className="stat-value offline">{stats?.offline_miners || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">总算力</div>
            <div className="stat-value">{formatHashrate(stats?.total_hashrate || null)}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">总功耗</div>
            <div className="stat-value">{stats?.total_power?.toFixed(0) || 0} W</div>
          </div>
        </div>
        <button
          className="discover-btn"
          onClick={handleDiscover}
          disabled={discovering}
        >
          {discovering ? '发现中...' : '发现新矿机'}
        </button>
      </div>

      <div className="miners-grid">
        {miners.map((miner) => (
          <div
            key={miner.id}
            className="miner-card"
            onClick={() => navigate(`/miner/${miner.id}`)}
          >
            <div className="miner-card-header">
              <div className="miner-title">
                <h3>{miner.hostname || miner.ip_address}</h3>
                <span className="miner-model">{miner.model || '未知型号'}</span>
              </div>
              <div
                className="status-indicator"
                style={{ backgroundColor: getStatusColor(miner.is_online) }}
              />
            </div>

            {miner.latest_status && (
              <div className="miner-stats">
                <div className="stat-row">
                  <span className="stat-label">IP地址:</span>
                  <span className="stat-value">{miner.ip_address}</span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">算力:</span>
                  <span className="stat-value">
                    {formatHashrate(miner.latest_status.hashrate_5s)}
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">温度:</span>
                  <span className="stat-value">
                    {miner.latest_status.temp_chip || '--'}°C
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">功耗:</span>
                  <span className="stat-value">
                    {miner.latest_status.power_consumption?.toFixed(0) || '--'} W
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">运行时间:</span>
                  <span className="stat-value">
                    {formatUptime(miner.latest_status.uptime)}
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">矿池状态:</span>
                  <span
                    className={`stat-value ${
                      miner.latest_status.pool_status === 'Alive' ? 'online' : 'offline'
                    }`}
                  >
                    {miner.latest_status.pool_status || '未知'}
                  </span>
                </div>
              </div>
            )}

            {!miner.latest_status && (
              <div className="no-status">暂无状态数据</div>
            )}
          </div>
        ))}
      </div>

      {miners.length === 0 && (
        <div className="empty-state">
          <p>暂无矿机数据</p>
          <button className="discover-btn" onClick={handleDiscover}>
            发现矿机
          </button>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

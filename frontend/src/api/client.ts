import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Miner {
  id: number;
  ip_address: string;
  model: string | null;
  hostname: string | null;
  mac_address: string | null;
  is_online: boolean;
  last_seen: string | null;
  latest_status: MinerStatus | null;
}

export interface MinerStatus {
  timestamp: string;
  temp_chip: number | null;
  temp_pcb: number | null;
  temp_max: number | null;
  power_consumption: number | null;
  humidity: number | null;
  hashrate: number | null;
  hashrate_5s: number | null;
  hashrate_avg: number | null;
  fan_speed_1: number | null;
  fan_speed_2: number | null;
  fan_speed_3: number | null;
  fan_speed_4: number | null;
  pool_url: string | null;
  pool_user: string | null;
  pool_status: string | null;
  uptime: number | null;
  network_status: string | null;
  hasboard_info: HashboardInfo[];
}

export interface HashboardInfo {
  id: number;
  status: string;
  temperature: number;
  hashrate: string;
  chip_temp: number;
  pcb_temp: number;
  fan_speed: number;
  chain: string;
}

export interface MinerDetail extends Miner {
  history: HistoryPoint[];
  logs: LogEntry[];
}

export interface HistoryPoint {
  timestamp: string;
  temp_chip: number | null;
  temp_pcb: number | null;
  hashrate: number | null;
  power_consumption: number | null;
}

export interface LogEntry {
  id: number;
  timestamp: string;
  log_level: string;
  message: string;
  source: string;
}

export interface Stats {
  total_miners: number;
  online_miners: number;
  offline_miners: number;
  total_hashrate: number;
  total_power: number;
}

export const api = {
  getMiners: async (): Promise<Miner[]> => {
    const response = await apiClient.get('/api/miners');
    return response.data;
  },

  getMinerDetail: async (id: number): Promise<MinerDetail> => {
    const response = await apiClient.get(`/api/miners/${id}`);
    return response.data;
  },

  getMinerStatus: async (id: number): Promise<any> => {
    const response = await apiClient.get(`/api/miners/${id}/status`);
    return response.data;
  },

  discoverMiners: async (): Promise<any> => {
    const response = await apiClient.post('/api/miners/discover');
    return response.data;
  },

  getStats: async (): Promise<Stats> => {
    const response = await apiClient.get('/api/stats');
    return response.data;
  },
};

export default apiClient;

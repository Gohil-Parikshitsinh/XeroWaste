export interface InventoryItem {
  id: string;
  name: string;
  quantity: number;
  expiryDate?: string;
  status: 'fresh' | 'expiring-soon' | 'expired';
}

export interface DetectionResult {
  items: InventoryItem[];
  timestamp: string;
}
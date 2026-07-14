import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
    
    def train_step(self, state, action, reward, next_state, done):
        """
        Train the model on a single step or batch of steps
        """
        # Convert to tensors
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        done = torch.tensor(done, dtype=torch.bool)  # Fixed: use bool tensor
        
        # Handle single sample vs batch
        if len(state.shape) == 1:
            # Single sample - add batch dimension
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = torch.unsqueeze(done, 0)
        
        # 1. Get current Q values
        pred = self.model(state)  # Shape: (batch_size, output_size)
        
        # 2. Get target Q values
        with torch.no_grad():  # FIXED: No gradients needed for target
            target = pred.clone()
            
            # Get Q values for next states
            next_q_values = self.model(next_state)  # Shape: (batch_size, output_size)
            max_next_q = torch.max(next_q_values, dim=1)[0]  # Shape: (batch_size,)
            
            # Update target values
            for idx in range(len(done)):
                if done[idx]:
                    target[idx][action[idx].item()] = reward[idx]
                else:
                    target[idx][action[idx].item()] = reward[idx] + self.gamma * max_next_q[idx]
        
        # 3. Calculate loss and update
        self.optimizer.zero_grad()
        loss = self.criterion(pred, target)
        loss.backward()
        self.optimizer.step()
        
        return loss.item()  # Return loss for logging

class ImprovedQTrainer:
    """
    Improved version with batch training and target network support
    """
    def __init__(self, model, target_model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.target_model = target_model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        self.loss_history = []
    
    def train_step(self, state, action, reward, next_state, done):
        """
        Train using Double DQN approach with target network
        """
        # Convert to tensors
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        done = torch.tensor(done, dtype=torch.bool)
        
        # Handle batch dimensions
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = torch.unsqueeze(done, 0)
        
        # Current Q values
        current_q = self.model(state)
        
        # Target Q values using Double DQN
        with torch.no_grad():
            # Get best action from current model
            next_q = self.model(next_state)
            best_actions = torch.argmax(next_q, dim=1)  # Shape: (batch_size,)
            
            # Get Q values from target model for those actions
            target_next_q = self.target_model(next_state)
            target_q_values = target_next_q.gather(1, best_actions.unsqueeze(1)).squeeze(1)
            
            # Compute target
            target = current_q.clone()
            for idx in range(len(done)):
                if done[idx]:
                    target[idx][action[idx].item()] = reward[idx]
                else:
                    target[idx][action[idx].item()] = reward[idx] + self.gamma * target_q_values[idx]
        
        # Update model
        self.optimizer.zero_grad()
        loss = self.criterion(current_q, target)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)  # Gradient clipping
        self.optimizer.step()
        
        self.loss_history.append(loss.item())
        return loss.item()
    
    def update_target_network(self):
        """Copy weights from model to target network"""
        self.target_model.load_state_dict(self.model.state_dict()) 
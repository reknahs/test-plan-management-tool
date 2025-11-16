/**
 * Test Plan Management Tool - Frontend React Application
 *
 * Main React component that provides a complete interface for managing test plans:
 * - View, create, edit, and delete test plans
 * - Manage individual test steps within plans
 * - AI-generated test suggestions from documents
 * - Real-time loading states and error handling
 *
 * Architecture: React hooks-based state management with Axios for API communication
 * Backend Integration: FastAPI REST API on localhost:8000
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Backend API configuration
const API_BASE = 'http://localhost:8000';  // FastAPI server URL

function App() {
  // State management for test plans data and UI state

  // List of all test plans fetched from backend API
  const [plans, setPlans] = useState([]);

  // ID of the plan currently being edited (null when creating new plan)
  const [editingPlan, setEditingPlan] = useState(null);

  // Text document input for AI suggestions
  const [suggestDoc, setSuggestDoc] = useState('');

  // AI-generated test steps from document analysis
  const [suggestedSteps, setSuggestedSteps] = useState([]);

  // AI-generated title for the suggested test plan
  const [suggestedTitle, setSuggestedTitle] = useState('');

  // AI-generated description for the suggested test plan
  const [suggestedDescription, setSuggestedDescription] = useState('');

  // Loading state for AI generation process
  const [isGenerating, setIsGenerating] = useState(false);

  // Form state for creating/editing test plans
  const [form, setForm] = useState({ title: '', description: '', steps: [] });

  // Fetch test plans on component mount
  useEffect(() => {
    fetchPlans();
  }, []);

  /**
   * Fetch all test plans from the backend API and update state
   */
  const fetchPlans = async () => {
    const res = await axios.get(`${API_BASE}/plans`);
    setPlans(res.data);
  };

  /**
   * Create a new test plan by sending form data to backend
   * Updates local state with new plan and clears form
   * Validation: Requires title field
   */
  const handleCreate = async () => {
    if (!form.title) return;  // Prevent creation without title
    try {
      const res = await axios.post(`${API_BASE}/plans`, form);
      setPlans([...plans, res.data]);  // Add new plan to local state
      resetForm();  // Clear form for next entry
    } catch (err) {
      console.error(err);
    }
  };

  /**
   * Update existing test plan via PUT request
   * Replaces plan in local state with updated version
   */
  const handleEdit = async () => {
    if (!form.title) return;
    try {
      const res = await axios.put(`${API_BASE}/plans/${editingPlan}`, form);
      // Update plan in state by replacing matching ID
      setPlans(plans.map(p => p.id === res.data.id ? res.data : p));
      resetForm();
    } catch (err) {
      console.error(err);
    }
  };

  /**
   * Delete test plan and remove from local state
   */
  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_BASE}/plans/${id}`);
      // Filter out deleted plan from state
      setPlans(plans.filter(p => p.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const startEdit = (plan) => {
    setEditingPlan(plan.id);
    setForm({ ...plan });
  };

  const addStep = () => {
    setForm({ ...form, steps: [...form.steps, { description: '' }] });
  };

  const updateStep = (index, desc) => {
    const newSteps = [...form.steps];
    newSteps[index] = { description: desc };
    setForm({ ...form, steps: newSteps });
  };

  const deleteStep = (index) => {
    const newSteps = form.steps.filter((_, i) => i !== index);
    setForm({ ...form, steps: newSteps });
  };

  const resetForm = () => {
    setForm({ title: '', description: '', steps: [] });
    setEditingPlan(null);
  };

  const handleSuggest = async () => {
    if (!suggestDoc.trim()) return; // Don't generate if no text
    
    setIsGenerating(true);
    setSuggestedTitle('');
    setSuggestedDescription('');
    setSuggestedSteps([]);
    
    try {
      const res = await axios.post(`${API_BASE}/suggest`, { document: suggestDoc });
      setSuggestedTitle(res.data.title);
      setSuggestedDescription(res.data.description);
      setSuggestedSteps(res.data.steps);
    } catch (err) {
      console.error(err);
      setSuggestedTitle('Error Generating Plan');
      setSuggestedDescription('Failed to generate suggestions');
      setSuggestedSteps(['Please check if Ollama is running and the mistral model is available']);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="App">
      <h1>Test Plan Management Tool</h1>
      <section>
        <h2>Test Plans</h2>
        <ul>
          {plans.map(plan => (
            <li key={plan.id}>
              <h3>{plan.title}</h3>
              <p>{plan.description}</p>
              <ul>
                {plan.steps.map((step, idx) => (
                  <li key={idx}>{step.description}</li>
                ))}
              </ul>
              <button onClick={() => startEdit(plan)}>Edit</button>
              <button onClick={() => handleDelete(plan.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>{editingPlan ? 'Edit' : 'Create'} Plan</h2>
        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <textarea
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <h4>Test Steps</h4>
        {form.steps.map((step, idx) => (
          <div key={idx}>
            <input
              type="text"
              value={step.description}
              onChange={(e) => updateStep(idx, e.target.value)}
            />
            <button onClick={() => deleteStep(idx)}>Delete</button>
          </div>
        ))}
        <button onClick={addStep}>Add Step</button>
        <button onClick={editingPlan ? handleEdit : handleCreate}>
          {editingPlan ? 'Save' : 'Create'}
        </button>
        <button onClick={resetForm}>Cancel</button>
      </section>

      <section>
        <h2>Suggest Test Steps</h2>
        <textarea
          placeholder="Enter document text to suggest test steps"
          value={suggestDoc}
          onChange={(e) => setSuggestDoc(e.target.value)}
        />
        <button onClick={handleSuggest} disabled={isGenerating}>
          {isGenerating ? 'Generating...' : 'Get Suggestions'}
        </button>
        {isGenerating && <p style={{ color: 'blue' }}>⏳ Generating test plan suggestions...</p>}
        <ul>
          {!isGenerating && suggestedSteps.map((step, idx) => (
            <li key={idx}>{step}</li>
          ))}
          {isGenerating && <li style={{ color: 'gray' }}>Waiting for AI response...</li>}
        </ul>
        <button onClick={() => {
          setForm({
            title: suggestedTitle,
            description: suggestedDescription,
            steps: suggestedSteps.map(s => ({ description: s }))
          });
          setEditingPlan(null);
        }} disabled={isGenerating || suggestedSteps.length === 0}>Import Suggestions as New Plan</button>
      </section>
    </div>
  );
}

export default App;

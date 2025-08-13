# Contributing to Cyra AI

Thank you for your interest in contributing to Cyra AI! This document provides guidelines for contributing to our cybersecurity assistant project.

## 🚀 Getting Started

### Prerequisites
- Basic knowledge of HTML, CSS, and JavaScript
- Understanding of responsive web design
- Familiarity with cybersecurity concepts (helpful but not required)

### Local Development Setup
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/your-username/cyra-ai.git

# Navigate to project directory
cd cyra-ai

# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Make your changes
# Test your changes locally
python -m http.server 8000

# Open http://localhost:8000 in your browser
```

## 📝 How to Contribute

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Provide browser and device information
- Include screenshots if applicable

### ✨ Feature Requests
- Open an issue with the "enhancement" label
- Describe the feature in detail
- Explain the use case
- Consider implementation complexity

### 🛠️ Code Contributions

#### Areas for Contribution
1. **UI/UX Improvements**
   - Enhance responsive design
   - Improve accessibility
   - Add animations and interactions
   - Optimize performance

2. **Content Enhancement**
   - Improve demo responses
   - Add cybersecurity educational content
   - Update feature descriptions
   - Enhance documentation

3. **Technical Improvements**
   - Code optimization
   - SEO enhancements
   - Browser compatibility
   - Performance optimizations

#### Code Standards
- Use semantic HTML5
- Follow CSS custom properties (CSS variables)
- Write vanilla JavaScript (no frameworks)
- Maintain responsive design principles
- Ensure accessibility compliance (WCAG 2.1)

#### Testing
- Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- Verify mobile responsiveness
- Check keyboard navigation
- Validate HTML and CSS
- Test with screen readers

## 📋 Pull Request Process

1. **Before Submitting**
   - Ensure your code follows the project standards
   - Test thoroughly on different devices/browsers
   - Update documentation if necessary
   - Verify no console errors

2. **Pull Request Guidelines**
   - Use a clear and descriptive title
   - Describe what changes you made and why
   - Reference related issues
   - Include screenshots for UI changes
   - Keep changes focused and atomic

3. **Review Process**
   - Maintainers will review your PR
   - Address feedback promptly
   - Be open to suggestions and improvements
   - Maintain a respectful tone

## 🎨 Design Guidelines

### Visual Design
- Follow the existing color scheme and gradients
- Maintain glassmorphism design language
- Use consistent spacing and typography
- Ensure high contrast for accessibility

### Animation Guidelines
- Use CSS animations and transitions
- Keep animations smooth (60fps)
- Provide reduced motion alternatives
- Don't overuse animations

### Responsive Design
- Mobile-first approach
- Breakpoints: 480px, 768px, 1024px, 1200px
- Touch-friendly interface elements
- Readable typography on all devices

## 🔧 Technical Guidelines

### File Organization
```
cyra-ai/
├── index.html          # Main landing page
├── README.md           # Project documentation
├── LICENSE             # MIT license
├── .github/
│   └── workflows/
│       └── deploy.yml  # GitHub Pages deployment
└── assets/             # Static assets (if needed)
```

### Performance Standards
- Lighthouse Performance Score: 90+
- First Contentful Paint: <1.5s
- Largest Contentful Paint: <2.5s
- Cumulative Layout Shift: <0.1
- Time to Interactive: <3s

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
- Mobile: iOS 13+, Android 8+

## 📖 Content Guidelines

### Writing Style
- Clear and concise language
- Professional but friendly tone
- Cybersecurity-focused content
- Accessible to different skill levels

### Demo Content
- Realistic cybersecurity scenarios
- Educational responses
- Helpful and actionable advice
- Current best practices

## 🎯 Priority Areas

### High Priority
- Mobile responsiveness improvements
- Accessibility enhancements
- Performance optimizations
- Content quality improvements

### Medium Priority
- New interactive features
- Enhanced animations
- Additional demo responses
- SEO improvements

### Low Priority
- Visual design tweaks
- Code refactoring
- Documentation updates
- Minor bug fixes

## 💬 Communication

### Discussion Channels
- GitHub Issues for bugs and features
- GitHub Discussions for general questions
- Pull Request comments for code review

### Getting Help
- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Tag maintainers if urgent

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## 📄 License

By contributing to Cyra AI, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make cybersecurity more accessible through Cyra AI!** 🛡️

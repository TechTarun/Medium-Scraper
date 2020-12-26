import React, { Component } from 'react';
import "./styles/App.css";
import SearchIcon from '@material-ui/icons/Search';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from 'axios';

class Navbar extends Component {
  render(){
    return (
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <span className="navbar-brand" style={{marginLeft: 15}}>Medium Scraper</span>
      </nav>
    )
  }
}

class MediumLogo extends React.Component{
  render(){
    return(
      <div className="container pagelogo">
      <img src="https://miro.medium.com/max/8978/1*s986xIGqhfsN8U--09_AdA.png" className="img-fluid" alt="Medium Logo" />
      </div>
    )
  }
}

class JobTable extends Component {
  constructor(props){
    super(props)
    this.state = {
      output: null
    }
    this.updateStatus = this.updateStatus.bind(this);
    this.handleOutput = this.handleOutput.bind(this);
    this.enableButton = this.enableButton.bind(this);
  }

  componentDidMount(){
    this.timerID = setInterval(() => this.updateStatus(), 6000)
  }

  componentWillUnmount(){
    clearInterval(this.timerID)
  }

  updateStatus(){
    this.setState({
      output: this.handleOutput(this.props.jobs)
    })
  }

  enableButton(){
    this.props.enableButton()
  }

  handleOutput(jobs){
    const data = {
      "job_id" : jobs
    }
    axios.post('http://c71ffd42e549.ngrok.io/scraper/api/crawl/status', data).then(
      res => {
        this.setState({
          output: res.data.message
        })

        var num_of_unfinished_jobs = 0;
        this.state.output.map((item) => {
          if(item === "running" || item === "pending"){
            num_of_unfinished_jobs += 1
          }
          return null;
        })
        if(num_of_unfinished_jobs === 0){
          clearInterval(this.timerID)
          this.enableButton()
        }
      }
    )
  }

  render(){
    var index = 0;
    if(this.state.output === null || this.state.output === undefined){
      return(
        <tbody></tbody>
      )
    }

    else{
      this.rows = this.state.output.map((item) => {
        if(item === "running" || item === "pending"){
          index += 1
          this.row = 
            <tbody>
                <tr key={index}>
                  <th scope="row">{index}</th>
                  <td>{item}</td>
                  <td></td>
                  <td></td>
                </tr>
            </tbody>
        }
        else{
          index += 1
          this.row = 
          <tbody>
            <tr key={index}>
              <th scope="row">{index}</th>
              <td><a href={item[3]}>{item[0]}</a></td>
              <td>{item[1]}</td>
              <td>{item[2]}</td>
            </tr>
          </tbody>
        }
        return this.row;
      })
      return (
        this.rows.map((item) => item)
      )
    }
  }
}

class Loader extends Component {
  render(){
    if(this.props.status.length === 0){
      return (
        <div></div>
      )
    }
    else{
      return(
        <div className="container"><CircularProgress /></div>
      )
    }
  }
}

class ShowTable extends Component {
  render(){
    const jobs = this.props.jobs
    if(jobs === null){
      return null
    }
    else{
      return (
        <div>
          <table className="table">
            <thead>
              <tr>
                <th scope="col">S. No.</th>
                <th scope="col">Blog Title</th>
                <th scope="col">Blog Author</th>
                <th scope="col">Blog Responses</th>
              </tr>
            </thead>
            <JobTable jobs={jobs} enableButton={this.props.enableButton}/>
          </table>
        </div>
      )
    }
  }
}

class CrawlButton extends Component{
  constructor(props){
    super(props);
    this.state = {
      message: null,
      unique_id: null,
      status: "",
      jobs: null,
      isButtonEnabled: false
    }
    this.handleClick = this.handleClick.bind(this);
    this.enableButton = this.enableButton.bind(this);
  }

  enableButton(){
    this.setState({
      isButtonEnabled: false
    })
  }

  handleClick(){
    if(this.props.tag.length === 0){
      alert("Please enter some tag to crawl")
    }
    else{
      this.setState({
        isButtonEnabled: true,
        status: "Initalizing crawls....",
        jobs: null
      })
      let data = {
        tag: this.props.tag
      }
      axios.post('http://c71ffd42e549.ngrok.io/scraper/api/crawl/links', data).then(
        res => {
          this.setState({
            status: "",
            unique_id: res.data.unique_id,
          })

          let data = {
            unique_id: this.state.unique_id
          }
          axios.post('http://c71ffd42e549.ngrok.io/scraper/api/crawl/blogs', data).then(
            res => {
            this.setState({
              jobs: res.data.jobs,
              isDone: false
            })
          }
          )
        }
      )
    }
  }

  render(){
    return(
      <div className="container">
        <button type="button" className="crawlbutton btn btn-outline-dark" onClick={this.handleClick} disabled={this.state.isButtonEnabled}>Crawl!!</button><br></br>
        {/* <div className="progressloader"><CircularProgress /></div> */}
        <div className="progressloader"><Loader status={this.state.status}/></div>

        <br></br>
        <ShowTable jobs={this.state.jobs} enableButton={this.enableButton}/>
      </div>
    )
  }
}

class TagInput extends Component{
  constructor(props){
    super(props)
    this.state = {
      tag: ""
    }
  }

  render(){
    return(
      <div className="container">
        <div className="container input-group mb-3 taginput">
          <div className="input-group-prepend">
            <span className="input-group-text" id="basic-addon1"><SearchIcon></SearchIcon></span>
          </div>
          <input type="text" className="form-control" placeholder="Enter tag or topic to search blogs!" value={this.state.tag} aria-label="Username" aria-describedby="basic-addon1" onChange={(event) => {
                this.setState({
                  tag: event.target.value
                })
          }}></input>
        </div>
        <CrawlButton tag={this.state.tag} resetInput={this.resetInput}/>
      </div>
    )
  }
}

class App extends Component {
  render() {
    return (
      <div>
        <Navbar />
        <MediumLogo />
        <TagInput />
      </div>
    );
  }
}

export default App;
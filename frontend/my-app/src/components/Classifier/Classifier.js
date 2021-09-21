import React, {Component} from 'react';
import Dropzone from 'react-dropzone';
import './Classifier.css'
import {Spinner, Button, Alert, Image} from 'react-bootstrap'
import axios from 'axios'
import image_1 from "../../static_media/1.png"

class Classifier extends Component {

    state = {
        files: [],
        isLoading: false,
        recentImage: null,
    }

    handleClick = () => {
        // you can now use this value to load your images
        this.setState({
            files: [],
            isLoading: true,
            recentImage: null
        })
        this.loadImage([image_1])
    }

    onDrop = (files) => {
        this.setState({
            files: [],
            isLoading: true,
            recentImage: null
        })
        this.loadImage(files)
    }

    loadImage = (files) => {
        setTimeout(() => {
            this.setState({
                files,
                isLoading: false
            }, () => {
                console.log(this.state.files)
            })
        }, 1000);
    }

    activateSpinner = () => {
        this.setState({
            files: [],
            isLoading: true,
        })
    }

    deactivateSpinner = () => {
        this.setState({isLoading: false})
    }

    sendImage = () => {
        this.activateSpinner()
        let formData = new FormData()
        formData.append('picture', this.state.files[0], this.state.files[0].name)
        axios.post('http://127.0.0.1:8000/api/images/', formData, {
            headers: {
                'accept': 'application/json',
                'content-type': 'multipart/form-data'
            }
        })
            .then(resp => {
                this.getImageClass(resp)
                console.log(resp.data.id)
            })
            .catch(err => {
                console.log(err)
            })
    }

    getImageClass = (obj) => {
        axios.get(`http://127.0.0.1:8000/api/images/${obj.data.id}/`, {
            headers: {
                'accept': 'application/json',
            }
        })
            .then(resp => {
                this.setState({recentImage: resp})
                console.log(resp)
            })
            .catch(err => {
                console.log(err)
            })
        this.deactivateSpinner()

    }


    render() {


        const files = this.state.files.map(file => (
            <li key={file.name}>
                {file.name} - {file.size} bytes
            </li>
        ));
        return (

            <Dropzone onDrop={this.onDrop} accept='image/png, image/jpeg' maxFiles={1}>
                {({isDragActive, getRootProps, getInputProps}) => (
                    <section className="container">
                        <div {...getRootProps({className: 'dropzone back'})}>
                            <input {...getInputProps()} />
                            <i className="far fa-image mb-2 text-muted" style={{fontSize: 100}}></i>
                            <p className='text-muted'>{isDragActive ? "Drop some images " : "Upload a Microcirculation image"}</p>
                        </div>

                        <p> File Name </p>

                        <link
                            href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css"
                            rel="stylesheet"/>
                        <div className="container">
                            <div className="row">
                                <div className="col-sm-4">
                                    <button
                                        data-prefix="1"
                                        onClick={this.handleClick}
                                        className="btn btn-primary">
                                        Sample 1
                                    </button>
                                </div>
                                <div className="col-sm-4">
                                    <button
                                        data-prefix="2"
                                        onClick={this.handleClick}
                                        className="btn btn-primary">
                                        Sample 2
                                    </button>
                                </div>
                                <div className="col-sm-4">
                                    <button
                                        data-prefix="3"
                                        onClick={this.handleClick}
                                        className="btn btn-primary">
                                        Sample 3
                                    </button>
                                </div>
                            </div>
                        </div>

                        <aside>
                            {files}
                        </aside>

                        {this.state.files.length > 0 &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage}>Select Image</Button>
                        }

                        {this.state.isLoading &&
                        <Spinner animation="border" role="status"></Spinner>
                        }


                        {this.state.recentImage &&
                        <React.Fragment>
                            <Alert variant='primary'>
                                {this.state.recentImage.data.classified}
                            </Alert>
                            <Image className='justify-content-center' src={this.state.recentImage.data.picture}
                                   height='100' rounded/>
                        </React.Fragment>
                        }
                    </section>
                )}
            </Dropzone>
        );
    }
}

export default Classifier;